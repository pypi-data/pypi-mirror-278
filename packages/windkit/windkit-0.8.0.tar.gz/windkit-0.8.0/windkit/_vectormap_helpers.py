# (c) 2022 DTU Wind Energy
"""Common tools used in vectormap.py and _vectormap_gml.py"""
import json
from enum import IntEnum
from inspect import cleandoc
from pathlib import Path

import pandas as pd

from .geospatial_imports import requires_geopandas
from .landcover import LandCoverTable

VECTORMAP_FILE_EXTENSIONS = [".map", ".gml", ".shp", ".gpkg"]
VECTORMAP_GEOM_COL = "geometry"
VECTORMAP_ELEV_COL = "elev"
VECTORMAP_ALT_ELEV_COL = {"ELEV", "elevation", "ELEVATION"}
VECTORMAP_ROUL_COL = "z0_left"
VECTORMAP_ROUR_COL = "z0_right"
VECTORMAP_ROU_COLS = (VECTORMAP_ROUL_COL, VECTORMAP_ROUR_COL)
VECTORMAP_IDL_COL = "id_left"
VECTORMAP_IDR_COL = "id_right"
VECTORMAP_ID_COLS = (VECTORMAP_IDL_COL, VECTORMAP_IDR_COL)
VECTORMAP_LMASKL_COL = "landmask_left"
VECTORMAP_LMASKR_COL = "landmask_right"
VECTORMAP_LMASK_COLS = (VECTORMAP_LMASKL_COL, VECTORMAP_LMASKR_COL)
VECTORMAP_META_COLS = [VECTORMAP_ELEV_COL] + list(VECTORMAP_ROU_COLS)
VECTORMAP_INLINE_LCTABLE_COLS = ("id", "d", "z0", "desc")
_MAP_TYPE_CODES = {
    "elevation": 0,
    "roughness": 1,
    "speedup": 2,
    "turning": 3,
    "flow_inclination": 4,
    "turbulence_intensity": 5,
    "landcover": 6,
    "displacement_height": 7,
    "landmask": 15,
    "fetch": 16,
}


class MapTypes(IntEnum):
    elevation = 0
    roughness = 1
    landcover = 6


_LR_COLS = {
    "roughness": VECTORMAP_ROU_COLS,
    "landcover": VECTORMAP_ID_COLS,
    "landmask": VECTORMAP_LMASK_COLS,
}


def _read_map_file_header_to_epsg_table():
    """Opens the map_file_header_to_epsg.json file and returns it as a dict"""

    with open(Path(__file__).parent / "map_file_header_to_epsg.json", "r") as f:
        return json.load(f)


def _z0_to_landcover(gdf):
    """Converts a roughness to landcover GeoDataFrame.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Geopandas dataframe with the columns 'z0_left' and 'z0_right'

    Returns
    -------
    tuple: (geopandas.GeoDataFrame, LandCoverTable):
        GeoDataFrame with ID's that are present in the lookup table
        and the LandCoverTable itself
    """
    if not _is_vectormap(gdf):
        raise TypeError(
            cleandoc(
                """This is not a GeoDataFrame. Perhaps you are passing in a combination of a GeoDataFrame and a landcover table?"""
            )
        )

    if not _is_z0(gdf):
        raise TypeError("Can only convert roughness map to landcover map")

    # fastest way to get unique values in pandas is in fortran order, hence K
    all_z0 = pd.unique(gdf[list(VECTORMAP_ROU_COLS)].values.ravel("K"))

    z0_to_id = {z0: lid for lid, z0 in enumerate(all_z0)}
    lct = {lid: {"z0": z0, "d": 0.0, "desc": ""} for z0, lid in z0_to_id.items()}
    convert_z0 = lambda cell: z0_to_id[cell]

    gdf = gdf[["geometry"]].assign(
        id_left=list(map(convert_z0, gdf.z0_left)),
        id_right=list(map(convert_z0, gdf.z0_right)),
    )

    return (gdf, LandCoverTable(lct))


def _landcover_to_z0(gdf, lctable):
    """Converts a landcover to roughness GeoDataFrame.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Geopandas dataframe with the columns 'id_left' and 'id_right'
    lctable: LandCoverTable
        LandCoverTable class with id's, roughnesses, displacements and a description

    Returns
    -------
    gdf: geopandas.GeoDataFrame:
        GeoDataFrame with columns 'z0_left' and 'z0_right'
    """
    if not _is_vectormap(gdf):
        raise TypeError("This is not a vectormap so can't convert!")

    if not _is_lc(gdf):
        raise TypeError("Can only convert landcover map to a roughness map!")

    # make sure we create a new gdf and don't assign to original
    gdf = gdf[["geometry"]].assign(
        z0_left=[lctable[id]["z0"] for id in gdf.id_left],
        z0_right=[lctable[id]["z0"] for id in gdf.id_right],
    )

    return gdf


def _is_vectormap(gdf):
    gpd = requires_geopandas()
    if not isinstance(gdf, gpd.GeoDataFrame):
        return False
    return True


def _is_lc(gdf):
    if all([i in gdf.columns for i in VECTORMAP_ID_COLS]):
        return True
    return False


def _is_lmask(gdf):  # pragma: no cover
    if all([i in gdf.columns for i in VECTORMAP_LMASK_COLS]):
        return True
    return False


def _is_z0(gdf):
    if all([i in gdf.columns for i in VECTORMAP_ROU_COLS]):
        return True
    return False


def _is_elev(gdf):
    if VECTORMAP_ELEV_COL in gdf.columns:
        return True
    return False


def _has_inline_lctable(gdf):
    if all([i in gdf.columns for i in VECTORMAP_INLINE_LCTABLE_COLS]):
        return True
    return False


def _get_map_type(gdf):  # pragma: no cover
    if _is_lc(gdf):
        return "landcover"
    elif _is_z0(gdf):
        return "roughness"
    elif _is_elev(gdf):
        return "elevation"
    elif _is_lmask(gdf):
        return "landmask"
    raise ValueError("Unable to identify map_type from column names.")


def explode_gdf(gdf):
    # The explode is needed for converting multipart geometries: wasp only support
    # single part geometries.
    # The reset index is needed so that each single geometry has a unique ID
    return gdf.explode(index_parts=True).reset_index(drop=True)
