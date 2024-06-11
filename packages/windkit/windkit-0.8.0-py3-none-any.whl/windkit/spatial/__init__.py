# (c) 2022 DTU Wind Energy
"""
A collection of functions for working with geospatial object supported by WindKit.

Supported objects include:

1. Vector Maps in the form of geopandas objects: GeoDataFrame's and GeoSeries's
2. Array-like data in the form of xarray objects: DataArray's and xarray.Dataset's.
   Four structures of array-like objects are supported:

   1. **point** (..., *point*) with x, y, and z-coordinates each of length *point*
   2. **stacked_point** (..., *stacked_point*) with x, y-coordiantes each of length *stacked_point*
   3. **cuboid** (..., *height*, *south_north*, *west_east*) this requires regular spacing in the *south_north* and *west_east* dimensions
   4. **raster** (..., *south_north*, *west_east*) this is an internal structure that behaves like a 2D **cuboid**
"""

from ._bbox import BBox
from ._cuboid import create_isotropic_cuboid, to_cuboid
from ._interpolation import (
    interp_structured_like,
    interp_unstructured,
    interp_unstructured_like,
    interpolate_to_grid,
)
from ._latitude import get_latitude

# nopycln: file
from ._point import to_point, to_stacked_point
from ._raster import to_raster
from ._struct import (
    get_spatial_struct,
    is_cuboid,
    is_point,
    is_raster,
    is_stacked_point,
    is_vertical,
)
from ._utm import *
from .decorators import stack_then_unstack
from .spatial import *

__all__ = [
    "add_crs",
    "are_spatially_equal",
    "BBox",
    "clip",
    "clip_with_margin",
    "crs_are_equal",
    "covers",
    "count_spatial_points",
    "get_crs",
    "mask",
    "nearest_points",
    "reproject",
    "warp",
    "create_dataset",
    "get_latitude",
    "interp_structured_like",
    "interp_unstructured",
    "interp_unstructured_like",
    "interpolate_to_grid",
    "spatial_stack",
    "spatial_unstack",
    "gdf_to_ds",
    "ds_to_gdf",
]
