# (c) 2022 DTU Wind Energy
"""
Module for point operations.
"""
import pandas as pd
import shapely
import xarray as xr

from windkit.geospatial_imports import requires_geopandas

from ..metadata import update_history
from ._bbox import BBox
from ._crs import get_crs
from ._dimensions import _point_dim, _stacked_point_dim, _vertical_dim, _xy_dims
from ._struct import (
    _from_scalar,
    get_spatial_struct,
    is_point,
    is_raster,
    is_stacked_point,
)
from ._vertical import has_height_coord


def to_point(obj):
    """Converts a WindKit xarray.Dataset or xarray.DataArray
    to 'point' structure

    NOTE: Objects that get round-tripped through this function will have a height
          dimension added to all variables, even if they didn't have them initially.
          If you wish to preserve the 2D nature of those fields, please use spatial_stack
          and spatial_unstack. To convert "to_point" and back respectively.

    Parameters
    ----------
    obj : xarray.Dataset, xarray.DataArray
        WindKit xarray.Dataset or xarray.DataArray containing
        spatial dimensions and CRS variable

    Returns
    -------
    xarray.Dataset, xarray.DataArray
        WindKit xarray.Dataset or xarray.DataArray as a
        'point' dataset or dataarray.
    """
    # Check if the object is a scalar
    obj = _from_scalar(obj)

    # Identify what kind of conversion, if any is needed

    if is_point(obj):  # Already point object
        return obj

    x_dim, y_dim = _xy_dims()
    point_dim = _point_dim()
    stacked_point_dim = _stacked_point_dim()
    vertical_dim = _vertical_dim()

    ##############################################
    # From here we know that we need to reprocess
    ##############################################
    hgt_dim = (vertical_dim,) if has_height_coord(obj) else ()
    stack_dims = hgt_dim

    if is_stacked_point(obj):
        stack_dims += (stacked_point_dim,)
    else:
        stack_dims += (y_dim, x_dim)

    # Add dimension if it is only a coordinate
    for dim in stack_dims:
        if dim not in obj.dims:  # pragma:no cover impossible_scenario
            obj = obj.expand_dims(dim)

    obj_out = obj.stack(**{point_dim: stack_dims}).reset_index(point_dim)

    # 'point' object shouldn't have the 'stacked_point' coordinate
    if is_stacked_point(obj):
        del obj_out.coords[stacked_point_dim]

    # Add spatial metadata back to object
    stack_coords = hgt_dim + (y_dim, x_dim)
    for coord in stack_coords:
        obj_out[coord].attrs = obj[coord].attrs

    if isinstance(obj_out, xr.Dataset):
        obj_out = update_history(obj_out)
    return obj_out


def to_stacked_point(obj):
    """Converts a WindKit dataset or dataarray to a 'stacked_point' structure

    Parameters
    ----------
    obj : xarray.Dataset, xarray.DataArray
        WindKit xarray.Dataset or DataArray containing
        spatial dimensions and CRS variable

    Returns
    -------
    xarray.Dataset, xaray.DataArray
        WindKit xarray dataset or dataarray as a 'stacked_point' structure
    """

    # check whether is a scalar
    obj = _from_scalar(obj)

    if is_stacked_point(obj):  # Already stacked_point object
        return obj

    x_dim, y_dim = _xy_dims()
    point_dim = _point_dim()
    stacked_point_dim = _stacked_point_dim()
    vertical_dim = _vertical_dim()

    ##############################################
    # From here we know that we need to reprocess
    ##############################################
    hgt_dim = (vertical_dim,) if has_height_coord(obj) else ()

    if is_point(obj):
        names = [*hgt_dim, stacked_point_dim]
        if has_height_coord(obj):
            stack = zip(
                obj[vertical_dim].values, zip(obj[y_dim].values, obj[x_dim].values)
            )
        else:
            stack = zip(zip(obj[y_dim].values, obj[x_dim].values))
        index = pd.MultiIndex.from_tuples(stack, names=names)
        out_obj = obj.drop_vars([y_dim, x_dim, *hgt_dim])
        out_obj[point_dim] = index
        out_obj = out_obj.unstack(point_dim)
        out_obj.coords[x_dim] = (
            stacked_point_dim,
            [x[1] for x in out_obj[stacked_point_dim].values],
        )
        out_obj.coords[y_dim] = (
            stacked_point_dim,
            [x[0] for x in out_obj[stacked_point_dim].values],
        )

        hgt_dim = (vertical_dim,) if has_height_coord(obj) else ()

        if len(hgt_dim) == 1:
            if isinstance(obj, xr.Dataset):
                for var in out_obj.data_vars:
                    if "_pwio_data_is_2d" in out_obj[var].attrs:
                        if out_obj[var].attrs["_pwio_data_is_2d"]:
                            out_obj[var] = out_obj[var].isel({vertical_dim: 0})
                        del out_obj[var].attrs["_pwio_data_is_2d"]

            del out_obj.coords[stacked_point_dim]

            for coord in out_obj.coords:
                if (coord != hgt_dim[0]) and (hgt_dim[0] in out_obj[coord].dims):
                    out_obj[coord] = out_obj[coord].isel({vertical_dim: 0}, drop=True)

    elif is_raster(obj):
        stack_dims = (y_dim, x_dim)

        # Add dimension if it is only a coordinate
        for dim in stack_dims:
            if dim not in obj.dims:  # pragma:no cover impossible_scenario
                obj = obj.expand_dims(dim)

        out_obj = obj.stack(**{stacked_point_dim: stack_dims}).reset_index(
            stacked_point_dim
        )
        # Add spatial metadata back to object
        for coord in stack_dims:
            out_obj[coord].attrs = obj[coord].attrs
    if isinstance(out_obj, xr.Dataset):
        out_obj = update_history(out_obj)

    return out_obj.drop_vars(stacked_point_dim, errors="ignore")


def _mask_point(
    obj, mask, drop=False, method="intersects", **kwargs
):  # pragma:no cover covered_in_public_method
    """

    Parameters
    ----------
    obj : xr.Dataset, xr.DataArray
        WindKit object of 'point' or 'stacked_point' structure
    mask : geopandas.GeoSeries, geopandas.GeoDataFrame
        Mask to subset object by
    drop : bool, optional
        Whether to drop masked out entries or keep them as 'empty'.
    method : str, optional
        Method to use to check whether the points are
        within the mask. Options are "intersects" and "within".
        By default "intersects" is used.

    Returns
    -------
    xarray.Dataset, xarray.DataArray
        Masked object.

    """
    gpd = requires_geopandas()
    obj = obj.copy()
    crs_obj = get_crs(obj)

    # windkit.spatial.bbox.BBox object is converted to gpd.GeoSeries
    # where the LinearRing is converted to Polygon
    if isinstance(mask, (BBox)):
        poly = shapely.geometry.Polygon(mask.ring.coords)
        mask = gpd.GeoSeries(poly, crs=mask.crs)

    if isinstance(mask, (shapely.geometry.Polygon)):
        mask = gpd.GeoSeries(mask, crs=crs_obj)

    # If mask is tuple or list we assume bounds (minx, miny, maxx, maxy)
    # With same CRS as obj
    if isinstance(mask, (tuple, list)):
        if len(mask) != 4:
            raise ValueError(
                "Got tuple/list of size {len(mask)}. "
                + "Bounds (minx, miny, maxx, maxy)"
                + " should be size 4!"
            )
        minx, miny, maxx, maxy = mask
        poly = shapely.geometry.Polygon(
            ((minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy))
        )
        mask = gpd.GeoSeries(poly, crs=crs_obj)

    # Ensure mask is gpd.GeoSeries or gpd.GeoDataFrame
    if not isinstance(mask, (gpd.GeoDataFrame, gpd.GeoSeries)):
        raise ValueError(
            f"mask type {type(mask)} not supported!"
            + " must be tuple of bounds (minx, miny, maxx, maxy), "
            + " windkit.BBox, geopandas.GeoDataFrame, "
            + " geopandas.GeoSeries or shapely.geometry.Polygon"
        )

    crs_mask = mask.crs

    if not crs_obj.equals(crs_mask):
        raise ValueError("CRS's are not equal!")

    struct = get_spatial_struct(obj)

    if struct == "point":
        pt_dim = _point_dim()
    elif struct == "stacked_point":
        pt_dim = _stacked_point_dim()

    x_dim, y_dim = _xy_dims()
    x, y = obj[x_dim].values, obj[y_dim].values

    pts = gpd.GeoSeries(gpd.points_from_xy(x, y), crs=crs_obj)

    if method == "intersects":
        pts_masked = pts.loc[pts.intersects(mask.unary_union)]
    elif method == "within":
        pts_masked = pts.loc[pts.within(mask.unary_union)]
    else:
        raise ValueError('method should be one of: ["intersects", "within"]')

    if drop:
        obj = obj.isel(**{pt_dim: pts_masked.index})
    else:
        obj = obj.where(obj[pt_dim].isin(pts_masked.index))

    return obj
