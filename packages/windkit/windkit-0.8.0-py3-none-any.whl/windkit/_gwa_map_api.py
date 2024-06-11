# (c) 2022 DTU Wind Energy
"""
Module that downloads elevation and roughness maps from the GWA map api
https://api.globalwindatlas.info/qgis-data/v1/corine_2018?points_str={query_string}.
https://api.globalwindatlas.info/cogs/esa_cci_2015.tif
https://api.globalwindatlas.info/cogs/srtmGL3003_plus_viewfinder_corrected_cog.tif

The landcover databases have standard conversion tables that are included in
``windkit/landcovertables``.
"""
import logging

import numpy as np
import requests
from shapely.geometry import Polygon

from .geospatial_imports import requires_geopandas
from .landcover import LandCoverTable
from .map_conversion.poly2lines import poly2lines
from .raster_map import read_raster_map
from .spatial import BBox, clip, get_crs, reproject, warp

logger = logging.getLogger(__name__)
LIST_RASTER_SOURCES = [
    "ESA_CCI",
    "Viewfinder",
]

LIST_VECTOR_SOURCES = [
    "CORINE",
]

LIST_COGS = {
    "ESA_CCI": "https://api.globalwindatlas.info/cogs/esa_cci_2015.tif",
    "Viewfinder": "https://api.globalwindatlas.info/cogs/srtmGL3003_plus_viewfinder_corrected_cog.tif",
}


def _get_raster_map_from_dtu(bbox, dataset="Viewfinder", safety_buffer=None):
    """
    Get map from Google Earth Engine. Currently, all maps
    are downloaded in EPSG:4326 coordinates, even if the
    source map is in different coordinates.

    Parameters
    ----------
    bbox : windkit.spatial.BBox
        Bounding box of the map to download. Must be in "EPSG:4326" coordinates.

    dataset : str, optional
        Dataset to retrieve, by default "NASADEM"

    band : str, optional
        Band to retrieve, by default None

    Returns
    -------
    da : xarray.DataArray
        DataArray with the map

    """
    if not isinstance(bbox, BBox):
        raise ValueError("bbox must be a BBox object or a windkit.spatial.BBox object.")

    if dataset not in LIST_RASTER_SOURCES:
        valid_sources = "','".join(LIST_RASTER_SOURCES)
        raise ValueError(
            f"There is no access implemented to dataset '{dataset}'. Valid options are ['{valid_sources}']."
        )

    if dataset not in ["Viewfinder"]:
        da = read_raster_map(LIST_COGS[dataset], map_type="landcover")
    else:
        da = read_raster_map(LIST_COGS[dataset], map_type="elevation")

    da = da.sortby(["south_north", "west_east"])
    source_crs = get_crs(da)
    bbox_source_crs = reproject(bbox, source_crs)

    bbox_safe = _add_safety_buffer(bbox_source_crs, safety_buffer)

    da = clip(da, bbox_safe)
    da_bbox = warp(da, get_crs(bbox))

    # clip latlon bbox to match exactly the input bbox
    da_bbox = clip(da_bbox, bbox)

    return da_bbox


def _add_safety_buffer(bbox, safety_buffer=None):
    """
    Adds a safety buffer to the bounding box to avoid artifacts at the border when warping.

    Parameters
    ----------
    bbox : wk.spatial.BBox
        The bounding box to which the safety buffer is to be added.
    safety_buffer : float, optional
        The size of the safety buffer. If None, it is set to 0.002 deg for geographic projections (about 200 m at the equator)
        and 200 m for metric projections.

    Returns
    -------
    bbox : wk.spatial.BBox
        The bounding box with the added safety buffer.
    """
    # some extra margins to make sure we select an area that is somewhat
    # larger than the requested square, so that there is no artifacts at the border
    if safety_buffer is None:
        if get_crs(bbox).is_geographic:
            safety_buffer = 0.002  # about 500 m at the equator
        else:
            safety_buffer = 200  # 50  in metric space

    xll, yll, xur, yur = bbox.bounds()
    west_east_width = np.abs(xll - xur)
    south_north_width = np.abs(yll - yur)

    if safety_buffer > west_east_width or safety_buffer > south_north_width:
        raise ValueError(
            "You should not buffer with more than the size of the bounding box itself. Reduce your safety_buffer."
        )

    return bbox.buffer(safety_buffer)


def _get_vector_map_from_dtu(bbox, dataset="CORINE", safety_buffer=None):
    """
    Get map from Google Earth Engine. Currently, all maps
    are downloaded in EPSG:4326 coordinates, even if the
    source map is in different coordinates.

    Parameters
    ----------
    bbox : windkit.spatial.BBox
        Bounding box of the map to download. Must be in "EPSG:4326" coordinates.

    dataset : str, optional
        Dataset to retrieve, by default "NASADEM"

    band : str, optional
        Band to retrieve, by default None

    Returns
    -------
    da : xarray.DataArray
        DataArray with the map

    """
    if not isinstance(bbox, BBox):
        raise ValueError("bbox must be a BBox object or a windkit.spatial.BBox object.")

    if dataset not in LIST_VECTOR_SOURCES:
        valid_sources = "','".join(LIST_VECTOR_SOURCES)
        raise ValueError(
            f"There is no access implemented to dataset '{dataset}'. Valid options are ['{valid_sources}']."
        )

    bbox_crs = get_crs(bbox)
    bbox_safe = _add_safety_buffer(bbox, safety_buffer)

    # get bigger bounding box in lat/lon to request from URL
    bb_latlon = bbox_safe.reproject_to_geographic()

    query_string = ";".join([f"{lon},{lat}" for lon, lat in bb_latlon.ring.coords])

    # full URL to submit
    url = f"https://api.globalwindatlas.info/qgis-data/v1/corine_2018?points_str={query_string}"
    data = requests.get(url)
    feats = data.json()["features"]

    if feats:
        gpd = requires_geopandas()
        # there is some items in feats so we convert the GeoJSON to a geopandas dataframe
        gdf = gpd.GeoDataFrame.from_features(data.json()["features"], crs="EPSG:4326")
        lct = LandCoverTable.get_table("CORINE")
        lct_gdf = gpd.GeoDataFrame.from_dict(lct, orient="index")
        gdf_bbox_crs = gdf.to_crs(bbox_crs)
        gdf_bbox_crs = gdf_bbox_crs.clip(Polygon(bbox.ring))
        comb = gdf_bbox_crs.set_index("id").join(lct_gdf)
    else:
        # feats was an empty list, so we return an error
        raise ValueError("No features found in the specified bbox!")

    # in the future we should return this as a polygon map
    # return PolygonMap(comb.explode().reset_index())
    return (poly2lines(comb.explode(index_parts=True).reset_index()), lct)
