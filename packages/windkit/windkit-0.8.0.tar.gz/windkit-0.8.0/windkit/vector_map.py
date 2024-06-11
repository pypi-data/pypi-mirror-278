# (c) 2022 DTU Wind Energy
"""
Readers and writers for vectormap objects.

VectorMaps are defined as collections of linestrings and metadata that represent either
elevations, or the land-cover information. When working with land-cover lines, an
additional LandCoverTable is required to map the land-cover ids to relevant parameters.

Here VectorMaps are represented as geopandas.GeoDataFrame objects. They can be read
from and written to several different formats to support interoperability with different
tools. We recommend using the Geopackage (.gpkg) format if you do not need to use one of
the other formats. For interoperability with WAsP, you should use the .map format for
elevation maps, and .gml for land-cover maps.
"""
import argparse
import logging
import re
import warnings
import zipfile
from collections import defaultdict
from importlib.metadata import version
from inspect import cleandoc
from pathlib import Path
from typing import Union

import numpy as np
import pyproj
from shapely.geometry import LineString, Polygon

from ._vectormap_gml import read_vector_map_gml, write_vectormap_gml
from ._vectormap_helpers import *
from ._vectormap_helpers import (
    _MAP_TYPE_CODES,
    _has_inline_lctable,
    _is_elev,
    _is_lc,
    _is_z0,
    _read_map_file_header_to_epsg_table,
    _z0_to_landcover,
)
from .geospatial_imports import requires_geopandas
from .landcover import LandCoverTable
from .map_conversion.poly2lines import poly2lines
from .spatial import BBox, crs_are_equal

logger = logging.getLogger("__name__")

__all__ = [
    "_MAP_TYPE_CODES",
    "read_vector_map",
    "vector_map_to_file",
    "create_flat_vector_map",
]


def _read_vector_map_combo(filename, crs, map_type):
    """
    Read a .map vector_map file, assuming that both elevation and
    roughness change values are present.

    Parameters
    ----------
    filename : str or pathlib.Path
        File path
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
    map_type: str {elevation, roughness, landmask}
        Which lines to read from the .map

    Returns
    -------
    tuple : (geopandas.GeoDataFrame, (geopandas.GeoDataFrame, LandCoverTable))
        Vectormap as a geodataframe with elevation data
        Vectormap as a geodataframe with landcover data
        LandCoverTable with lookup table for landcover data

    """

    metadata = ""
    n_lines = 0
    n_empty_lines = 0
    got_header_line = False
    current_point_count = 0
    ltype = -999
    n_pts_geom = None

    data = defaultdict(list)

    ###############
    # Setup maptype
    ###############
    # TODO: See about autodetecting map_type
    if map_type is None:
        raise ValueError(
            cleandoc(
                """'map_type' must be provided when reading .map file.
        You can use the read_roughness_map and read_elevation_map convience functions, or
        add a map_type argument."""
            )
        )
    map_type_code = _MAP_TYPE_CODES[map_type]
    if map_type == "landmask":
        map_type_code = _MAP_TYPE_CODES["roughness"]

    #############
    # Handle CRS
    #############
    if crs is None:
        crs = _crs_from_map_file(filename)
        if crs is None:
            raise ValueError("""'crs' cannot be detected from file""")

    with open(filename, "r", newline="\r\n") as fobj:
        # Read 4 header lines into a single string
        for _ in range(4):
            metadata += fobj.readline()

        # Process remaining data
        for line in fobj:
            elements = [float(i) for i in line.strip().split()]

            # Read line header
            if got_header_line is False:
                z0_left, z0_right, elev = np.nan, np.nan, np.nan

                # Check for empty lines
                if (
                    len(elements) == 0
                ):  # pragma: no cover (not sure what this should be)
                    n_pts_geom = 0
                    ltype = -999
                    n_empty_lines += 1

                # Check for list of points with no attributes
                if len(elements) == 1:
                    (n_pts_geom,) = elements
                    ltype = -999
                    n_empty_lines += 1

                # Elevation header row
                if len(elements) == 2:
                    elev, n_pts_geom = elements
                    ltype = 0

                # Roughness header line
                if len(elements) == 3:  # leave out the roughness line
                    z0_left, z0_right, n_pts_geom = elements
                    ltype = 1

                # Combination line
                if len(elements) == 4:
                    z0_left, z0_right, elev, n_pts_geom = elements
                    ltype = 2

                # Combination line with displacement height
                if len(elements) == 5:
                    raise RuntimeError(
                        ".map files with displacement heights are not supported."
                    )

                # Only save data if it is supposed to be output
                if ltype in [map_type_code, 2]:  # ltype=2 is combo line
                    if ltype == 0:
                        data[VECTORMAP_ELEV_COL].append(elev)
                    elif ltype == 1:
                        data[VECTORMAP_ROU_COLS[0]].append(z0_left)
                        data[VECTORMAP_ROU_COLS[1]].append(z0_right)
                    elif ltype == 2:
                        if map_type_code == 1:
                            data[VECTORMAP_ROU_COLS[0]].append(z0_left)
                            data[VECTORMAP_ROU_COLS[1]].append(z0_right)
                        else:
                            data[VECTORMAP_ELEV_COL].append(elev)

                    n_lines += 1

                x_pts = []
                y_pts = []

                got_header_line = True

            # if we have the header and the line is what we want
            # then get all the points.
            else:
                if ltype in [map_type_code, 2]:
                    x_pts += elements[0::2]
                    y_pts += elements[1::2]

                current_point_count += len(elements) / 2

                # After reading all the points for the line,
                # Set the header back to false and reset the point counter
                if current_point_count == n_pts_geom:
                    if ltype in [map_type_code, 2]:
                        geometry = LineString(zip(x_pts, y_pts))
                        data["geometry"].append(geometry)

                    got_header_line = False
                    current_point_count = 0

    if len(data) == 0:
        with open(filename, "r", newline="\r\n") as fobj:
            if len(fobj.readlines()) == 1:
                raise ValueError(
                    "Only a single line detected, make sure your mapfile has 'CRLF' line endings"
                )
        raise ValueError(f"""No '{map_type}' lines found.""")

    gpd = requires_geopandas()
    gdf = gpd.GeoDataFrame(
        {key: val for key, val in data.items() if len(val) > 0},
        geometry="geometry",
        crs=crs,
    ).dropna(axis=1, how="all")

    if map_type == "elevation":
        return gdf
    elif map_type == "roughness":
        gdf, lctable = _z0_to_landcover(gdf)
        return (gdf, lctable)
    elif map_type == "landmask":
        return gdf.rename(
            columns={
                VECTORMAP_ROUL_COL: VECTORMAP_LMASKL_COL,
                VECTORMAP_ROUR_COL: VECTORMAP_LMASKR_COL,
            }
        )


def read_vector_map(filename, crs=None, map_type=None, background_lc_id=None):
    """
    Read a vector_map from a file.

    Parameters
    ----------
    filename : str or pathlib.Path
        File path
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS` Default reads from file.
    map_type : str
        One of "elevation" or "roughness" to specify the type of map to create.
        Defaults to None.
    background_lc_id: int, optional.
        This option is used for polygon based landcover files. It sets the landcover id
        for all areas not covered by a polygon. The default is None, but if your area
        includes such areas, you should set it to an ID that is part of your landcover
        table.

    Returns
    -------
    gdf: geopandas.GeoDataFrame
        Vectormap as a geodataframe.
    lc : LandCoverTable
        LandCoverTable optional.
    """

    if isinstance(filename, zipfile.ZipExtFile):
        filetype = "ZipExtFile"
    else:
        filetype = Path(filename).suffix.lower()

        if not Path(filename).exists():
            raise FileNotFoundError(filename)

    ######################################################
    # We need custom handlers for .map and .gml filetypes
    ######################################################
    if filetype == ".map" or filetype == ".tmp":
        return _read_vector_map_combo(filename, crs=crs, map_type=map_type)
    elif filetype == ".gml":
        return read_vector_map_gml(filename)
    # the standard gdal way of storing elev is in capitals so it would be nice
    # to support that. The best way is to directly retrieve alternative names
    # from the metadata.py and the ALL_VARS_JSON, but here it is just hardcoded
    gpd = requires_geopandas()

    gdf = gpd.read_file(filename).rename(
        columns={v: VECTORMAP_ELEV_COL for v in VECTORMAP_ALT_ELEV_COL}
    )

    if crs is not None:
        if pyproj.CRS.from_user_input(gdf.crs) != pyproj.CRS.from_user_input(crs):
            raise ValueError(f"Dataset crs {gdf.crs} doesn't match crs argument {crs}.")

    #########################################
    # Convert polygons to lines if necessary
    #########################################
    if (np.array(gdf.geom_type) == "MultiPolygon").any() or (
        np.array(gdf.geom_type) == "Polygon"
    ).any():
        if background_lc_id is None:
            background_lc_id = -999
        gdf = poly2lines(gdf, background_lc_id)

    if _is_elev(gdf):
        gdf[VECTORMAP_ELEV_COL] = gdf[VECTORMAP_ELEV_COL].astype(float)
    if _is_z0(gdf):
        gdf[list(VECTORMAP_ROU_COLS)] = gdf[list(VECTORMAP_ROU_COLS)].astype(float)

    ###############################################
    # Get landcover table from file if it is there
    ###############################################
    if _is_lc(gdf):  # Requires separate landcover table, either from gpkg or json
        gdf[list(VECTORMAP_ID_COLS)] = gdf[list(VECTORMAP_ID_COLS)].astype(int)
        try:
            lcdf = gpd.read_file(filename, layer="landcover_table")
            if "index" in lcdf.columns:
                lcdf = lcdf.rename(columns={"index": "id"})
                warnings.warn(
                    "The use of the name 'index' to identify landcover ID's in the landcover table is deprecated, please use the name 'id' for this instead.",
                    FutureWarning,
                )
            lcdf = lcdf.set_index("id")
            lctable = LandCoverTable(
                lcdf.drop("geometry", axis=1).transpose().to_dict()
            )
        except ValueError:
            return gdf  # CHECK: should this return an lctable of None?

        return (gdf, lctable)

    if _has_inline_lctable(gdf):  # Landcover info is from each row of table
        lctable = LandCoverTable(
            gdf[["id", "d", "z0", "desc"]]
            .drop_duplicates()
            .set_index("id")
            .to_dict(orient="index")
        )
        return gdf, lctable

    return gdf


def vector_map_to_mapfile(gdf, filename, lctable=None, desc="WindKit", mode="w"):
    """
    Write vector_map in GeoDataFrame format to WAsP mapfile format.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Elevation or roughness change vector_map.
    filename : pathlib.Path or str
        Path to output file.
    lctable : LandCoverTable
        Landcover table to map landcover and roughness / displacements. Defaults to None.
    desc : str
        Description string added to the file (cannot be empty when reading with map editor).
        Defaults to "WindKit"
    mode : str("w" or "a")
        Write or append mode. Defaults to "w".
    """
    gdf = explode_gdf(gdf)
    if all(c in gdf.columns for c in VECTORMAP_META_COLS):  # pragma: no cover
        raise ValueError(
            cleandoc(
                """Both elevation and roughness values found! combo files are not supported! Please write them separately!"""
            )
        )

    if not _is_elev(gdf):
        raise ValueError("Only elevation data can be written to mapfile (.map) format.")

    if desc == "":
        raise ValueError("Description cannot be empty for a .map file.")
    map_type = "elevation"
    # build mapfile header
    mapeditor_crs_str = _crs_to_map_editor_str(gdf.crs)
    # Parse windkit version
    wk_version = version("windkit")
    ver_regex = r"(\d+)\.(\d+)\.(\d+)|(\d+)\.(\d+)"
    try:
        ver_str = re.match(ver_regex, wk_version, re.IGNORECASE).group()
    except:
        ver_str = ""
    header_str = f"+{desc} | {mapeditor_crs_str} | windkit v{ver_str}"

    with open(filename, mode, newline="\r\n") as fobj:
        # File header
        if mode == "w":
            fobj.write(header_str + "\n")
            # Fixed point #1 in user and metric [m] coordinates:
            # X1_user, Y1_user, X1_metric, Y1_metric
            fobj.write("%3.1f %3.1f %3.1f %3.1f\n" % (0.0, 0.0, 0.0, 0.0))

            # Fixed point #2 in user and metric [m] coordinates:
            # X2_user, Y2_user, X2_metric, Y2_metric
            fobj.write("%3.1f %3.1f %3.1f %3.1f\n" % (1.0, 0.0, 1.0, 0.0))

            # Scaling factor and offset for height scale (z),
            # Zmetric = scaling factor X (zuser +offset)
            fobj.write("%3.1f %15.1f\n" % (1.0, 0.0))

        for _, row in gdf.iterrows():
            rg = row.geometry
            x_pts, y_pts = (
                rg.boundary.coords.xy if isinstance(rg, Polygon) else rg.coords.xy
            )
            n_pts = len(x_pts)
            if map_type == "elevation":
                fobj.write(f"{row.elev:10.4f} {n_pts:10d}\n")
            xy_string = " ".join(f"{x:10.1f} {y:10.1f}" for x, y in zip(x_pts, y_pts))
            fobj.write(xy_string + "\n")


def vector_map_to_gmlfile(gdf, filename, lctable=None, desc="Windkit", **kwargs):
    """
    Write vectormap in GeoDataFrame format to GML format.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Elevation or roughness change vector_map.
    filename : pathlib.Path or str
        Path to output file.
    lctable : LandCoverTable
        Landcover table to map landcover and roughness / displacements. Defaults to None.
    desc : str
        Description added to the file (cannot be empty when reading with map editor).
        Defaults to "Windkit"
    kwargs : dict
        Extra arguments.

    """
    write_vectormap_gml(filename, gdf, lctable, desc)


def vector_map_to_file(
    gdf,
    filename: Union[Path, str],
    lctable: LandCoverTable = None,
    driver: str = "GPKG",
    **kwargs,
):
    """Write a GeoDataFrame vector map to a vectorfile.

    Filetypes are determined from the file extension.
    .map files passed to vector_to_mapfile()
    .gml files are passed to vector_to_gmlfile()
    all others use the geopandas .to_file() method

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Vector map to write
    filename : pathlib.Path or str
        Path to file to write to.
    lctable : LandCoverTable
        Landcover table to map landcover and roughness / displacements. Defaults to None.
    driver : str
        Name of the Fiona Driver to pass to geopandas.to_file(). Defaults to "GPKG"
    kwargs : dict
        Keyword arguments to pass to writer.
    """
    filename = Path(filename)
    filebase = filename.parent / filename.stem
    filetype = filename.suffix.lower()

    if not (_is_elev(gdf) or _is_lc(gdf)):
        raise ValueError("Only elevation or landcover maps can be written to file.")

    if _is_lc(gdf) and (lctable is None):
        raise ValueError("'lctable' not specified for landcover map")

    ########################################
    # Handle special cases of .map and .gml
    ########################################
    if filetype == ".map":
        return vector_map_to_mapfile(gdf, filename, **kwargs)
    elif filetype == ".gml":
        return vector_map_to_gmlfile(gdf, filename, lctable=lctable, **kwargs)
    elif filetype != ".gpkg":
        raise ValueError("Only .map, .gml and .gpkg formats are supported.")

    ############################################
    # We now are only handling GeoPackage files
    ############################################
    if _is_lc(gdf):
        logger.debug("Adding landcover table to GeoPackage output")

        gdf.to_file(str(filename), driver="GPKG", layer="landcover_lines")
        gpd = requires_geopandas()
        lct_gdf = gpd.GeoDataFrame.from_dict(lctable, orient="index")
        lct_gdf["geometry"] = None
        return lct_gdf.reset_index().to_file(
            str(filename), driver="GPKG", layer="landcover_table"
        )
    else:
        return gdf.to_file(str(filename), driver="GPKG")


def create_flat_vector_map(
    crs, dist=None, bbox=None, map_type="elevation", elev=0.0, z0_change=(0.0, 0.0)
):
    """
    Create a square flat elevation map, with bbox (-dist, -dist, dist, dist).

    Parameters
    ----------
    crs : str
        Spatial Reference System for projection information.
    dist : postive float
        1/2 the length of a single side of the map (Either this or bbox must be set).
    bbox : BBox
        Bounding box to use for setting the boundary rather than using dist. Defaults
        to None.
    map_type : str
        One of "elevation" or "roughness" to specify the type of map to create. Defaults
        to "elevation".
    elev : float
        Elevation to set the line to if it is an elevation map. Defaults to 0.0.
    z0_change : array of 2 floats
        Left and right z0 values for the line. Defaults to (0.0,0.0).

    Returns
    -------
    vector_map: geopandas.GeoDataFrame
        Flat vector_map
    """
    if bbox is not None and dist is not None:
        raise ValueError("You must specify only one of bbox and dist.")
    if bbox is None and dist is None:
        raise ValueError("You must specify one of bbox or dist")

    if dist is not None:
        pos_dist = abs(dist)
        neg_dist = pos_dist * -1
        bbox = BBox.from_cornerpts(neg_dist, neg_dist, pos_dist, pos_dist, crs)

    minx, miny, maxx, maxy = bbox.bounds()

    z0_left, z0_right = z0_change

    data = defaultdict(list)

    if map_type == "elevation":
        data[VECTORMAP_ELEV_COL].append(elev)
    elif map_type == "roughness":
        data[VECTORMAP_ROUL_COL].append(z0_left)
        data[VECTORMAP_ROUR_COL].append(z0_right)

    geometry = LineString(
        [
            (minx, miny),
            (maxx, miny),
            (maxx, maxy),
            (minx, maxy),
            (minx, miny),
        ]
    )

    data["geometry"].append(geometry)
    gpd = requires_geopandas()
    gdf = gpd.GeoDataFrame(data, geometry="geometry", crs=crs)

    if map_type == "elevation":
        return gdf

    return _z0_to_landcover(gdf)


def _split_combo_parser():
    """
    Parser for the split_combo command line tool
    """
    p = argparse.ArgumentParser(
        description="Split a combo mapfile into elevation and roughness GML files."
    )
    p.add_argument("inputfile", help="File to split")
    p.add_argument(
        "crs", help="Projection of the map, can be an epsg code, proj4 string, or wkt"
    )

    return p


def split_combo():
    """
    Split a combo mapfile into elevation and roughness files.

    The roughness and elevation files have the same name as the
    input file, but with _elev or _rou added at the end.
    """
    p = _split_combo_parser()
    args = p.parse_args()

    inputfile = args.inputfile
    try:
        crs = int(args.crs)
    except ValueError:
        crs = args.crs

    # Roughness
    lc_map, lc_table = read_vector_map(inputfile, crs, "roughness")
    vector_map_to_file(lc_map, inputfile[:-4] + "_landcover.gpkg", lc_table)

    # Elevation
    elev = read_vector_map(inputfile, crs, "elevation")
    vector_map_to_file(elev, inputfile[:-4] + "_elevation.gpkg")


def _crs_from_map_file(filename):
    """
    Gets crs/epsg from .map file

    Parameters
    ----------
    filename : pathlib.Path or str
        Path to .map file

    Returns
    -------
    crs: int
        Integer representing EPSG zone
    """
    gpd = requires_geopandas()
    if Path(filename).suffix == ".gml":
        gdf = gpd.read_file(filename, driver="GML", layer="ChangeLine")
        crs = gdf.crs.to_epsg()
    else:
        f = open(filename, "r", newline="\r\n")
        header = f.readline()
        f.close()

        epsg_lookup_table = _read_map_file_header_to_epsg_table()

        crs = None
        for string, epsg in epsg_lookup_table.items():
            if string in header:
                crs = epsg
                break

    return crs


def _crs_to_map_editor_str(crs):
    """
    Returns a CRS string with the map editor format
    to write in a .map file header

    Parameters
    ----------
    crs: pyproj.CRS.crs
        crs object to transform
    Returns
    -------
    crs_str : str
        String with the .map header format
    """
    epsg_lookup_table = _read_map_file_header_to_epsg_table()

    crs_str_lookup_table = {v: k for k, v in epsg_lookup_table.items()}
    for k, v in crs_str_lookup_table.items():
        if crs_are_equal(k, crs):
            return v
    return ""
