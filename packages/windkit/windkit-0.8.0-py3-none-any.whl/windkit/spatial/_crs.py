# (c) 2022 DTU Wind Energy
"""
Coordinate Reference System (CRS) library for working with
pyproj.crs.CRS objects in WindKit
"""
import warnings

import numpy as np
import pyproj
import xarray as xr

from windkit.geospatial_imports import requires_geopandas

from ..metadata import ALL_VARS_META
from ._bbox import BBox

_PRJ_XY_COORDS = {
    "west_east": ALL_VARS_META["west_east_proj"],
    "south_north": ALL_VARS_META["south_north_proj"],
}

_GEOG_XY_COORDS = {
    "west_east": ALL_VARS_META["west_east_geog"],
    "south_north": ALL_VARS_META["south_north_geog"],
}


def get_crs(obj):
    """Returns a pyproj.crs.CRS object from object metadata.

    This helper function allows gets the Coordinate Reference System (CRS)
    from any WindKit object.

    Parameters
    ----------
    obj : geopandas.GeoDataFrame, geopandas.GeoSeries,xarray.DataArray,xarray.Dataset or BBox
        Object to get CRS from.

    Returns
    -------
    CRS
        CRS object
    """

    if isinstance(obj, (xr.Dataset, xr.DataArray)):
        if "crs" in obj.coords:
            crs = pyproj.CRS.from_wkt(obj.crs.attrs["crs_wkt"])
        elif "epsg" in obj.attrs:
            warnings.warn(
                "The use of EPSG to identify CRS is deprecated, please use CF "
                + "conventions through pyproj.CRS",
                FutureWarning,
            )
            crs = pyproj.CRS.from_epsg(obj.attrs["epsg"])
        else:
            raise ValueError("no CRS found on object!")
        return crs

    gpd = requires_geopandas()
    if isinstance(obj, (BBox, gpd.GeoDataFrame, gpd.GeoSeries)):
        crs = obj.crs

    return crs


def add_crs(obj, crs):
    """Adds a Coordinate Reference System to a WindKit object.

    This helper function either adds or updates a crs coordinate on
    an existing object.

    Parameters
    ----------
    obj : geopandas.GeoDataFrame, geopandas.GeoSeries,xarray.DataArray,xarray.Dataset or BBox
        Object to set CRS on.
    crs : int, dict, str or CRS
        Value to create CRS object or an existing CRS object

    Returns
    -------
    same as obj
        Returns the same object with the updated CRS.

    """
    if isinstance(obj, (xr.Dataset, xr.DataArray)):
        obj.coords["crs"] = np.byte(0)

        pyproj_crs = pyproj.CRS.from_user_input(crs)
        # Check if user input matches an EPSG code, and use that if it does
        try:
            pyproj_crs = pyproj.CRS.from_epsg(pyproj_crs.to_epsg())
        except pyproj.exceptions.CRSError:
            pass

        crs_cf_dict = pyproj_crs.to_cf()
        crs_cf_dict["long_name"] = "CRS definition"
        # Needed for GDAL compliance
        crs_cf_dict["spatial_ref"] = pyproj_crs.to_wkt("WKT1_GDAL")
        obj.crs.attrs = crs_cf_dict

        # Update spatial coordinate metadata
        if pyproj_crs.is_projected:
            obj.coords["south_north"].attrs = _PRJ_XY_COORDS["south_north"]
            obj.coords["west_east"].attrs = _PRJ_XY_COORDS["west_east"]
        else:
            obj.coords["south_north"].attrs = _GEOG_XY_COORDS["south_north"]
            obj.coords["west_east"].attrs = _GEOG_XY_COORDS["west_east"]
        return obj

    gpd = requires_geopandas()
    if isinstance(obj, (BBox, gpd.GeoDataFrame, gpd.GeoSeries)):
        obj.crs = crs

    return obj


def crs_are_equal(obj_a, obj_b):
    """Check if CRS's of two WindKit objects are equal

    Parameters
    ----------
    obj_a, obj_b : int, dict, str, CRS, geopandas.GeoDataFrame, geopandas.GeoSeries,xarray.DataArray,xarray.Dataset
        Object to compare.

    Returns
    -------
    bool
        True if the CRS's are equal. False otherwise.

    """
    objects = [obj_a, obj_b]
    crs_list = []
    for obj in objects:
        if isinstance(obj, (int, str, dict, tuple, pyproj.CRS)):
            crs = pyproj.CRS.from_user_input(obj)
        else:
            crs = get_crs(obj)
        crs_list.append(crs)
    crs_a, crs_b = crs_list
    return crs_a.equals(crs_b)
