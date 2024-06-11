# (c) 2022 DTU Wind Energy
"""
Public interface to all of the spatial tools in WindKit
"""

import logging
import warnings

import numpy as np
import pyproj
import xarray as xr
from scipy.spatial import KDTree

from windkit.geospatial_imports import is_GeoDataFrame, is_GeoSeries, requires_geopandas

from ..metadata import _GLOBAL_CONVENTIONS, ALL_VARS_META, update_history
from ._bbox import BBox
from ._crs import add_crs, crs_are_equal, get_crs
from ._dimensions import _point_dim, _stacked_point_dim, _vertical_dim, _xy_dims
from ._point import _mask_point, is_point, is_stacked_point, to_point, to_stacked_point
from ._raster import _bounds as _raster_bounds
from ._raster import (
    _can_be_raster,
    _clip_to_bbox_raster,
    _has_raster_dims,
    _mask_raster,
)
from ._raster import _resolution as _raster_resolution
from ._raster import _warp_raster, is_raster, to_raster
from ._struct import _from_scalar, get_spatial_struct, is_cuboid
from ._vector import _clip_vector
from ._vertical import has_height_coord, has_height_dim

__all__ = [
    "add_crs",
    "are_spatially_equal",
    "BBox",
    "clip",
    "clip_with_margin",
    "crs_are_equal",
    "create_dataset",
    "count_spatial_points",
    "equal_spatial_shape",
    "get_crs",
    "mask",
    "reproject",
    "spatial_stack",
    "spatial_unstack",
    "warp",
    "nearest_points",
    "covers",
    "gdf_to_ds",
    "ds_to_gdf",
]

logger = logging.getLogger(__name__)


def count_spatial_points(obj):
    """Get the number of spatial points for a dataset or DataArray

    Parameters
    ----------
    obj: xarray.Dataset, xarray.DataArray
        WindKit xarray dataset or dataarray containing spatial dimensions.

    Raises
    ------
    ValueError
        Undetectable spatial structure
    """
    obj = _from_scalar(obj)
    dims = obj.sizes

    # Get dimension names
    xdim, ydim = _xy_dims()
    pt_dim = _point_dim()
    vert_dim = _vertical_dim()
    spt_dim = _stacked_point_dim()

    if is_cuboid(obj):
        return dims[vert_dim] * dims[ydim] * dims[xdim]
    elif is_raster(obj):
        return dims[ydim] * dims[xdim]
    elif is_stacked_point(obj):
        return dims[vert_dim] * dims[spt_dim]
    elif is_point(obj):
        return dims[pt_dim]
    else:
        raise ValueError("Unknown data structure cannot count points.")


def are_spatially_equal(obj_a, obj_b):
    """Checks that the spatial points are equivalent for both datasets

    Parameters
    ----------
    obj_a, obj_b : xarray.Dataset, xarray.DataArray
        WindKit xarray dataset or dataarray containing spatial
        dimensions and CRS variable

    Returns
    -------
    bool
        True if spatial coords are numpy.allclose

    """
    x_dim, y_dim = _xy_dims()

    if obj_a.coords[x_dim].size != obj_b.coords[x_dim].size:
        return False
    if obj_a.coords[y_dim].size != obj_b.coords[y_dim].size:
        return False
    return np.allclose(obj_a[x_dim], obj_b[x_dim]) and np.allclose(
        obj_a[y_dim], obj_b[y_dim]
    )


def create_dataset(west_east, south_north, height, crs, struct="auto", thresh=1e-9):
    """Create a WindKit dataset given a set of locations.

    Parameters
    ----------
    west_east : array_like
        1D array of west_east locations of interest
    south_north : array_like
        1D array of south_north locations of interest
    height : array_like
        Array of heights to create in output WindKit xarray dataset
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
    struct : str
        Used to specify the type of dataset that is desired
        Valid values are 'auto', 'cuboid', 'point' and
        'stacked_point'. The default value of 'auto' tries to create a cuboid,
        but falls back to point depending on the values specified.
    thresh : float
        Threshold value for raster detection
        Default set to 1e-9 m

    Returns
    -------
    xarray.Dataset
        WindKit formated zero-filled Dataset with one variable "output"
        and with the grid dimensions specified

    Notes
    -----
    This function will create a WindKit formatted dataset including all of the
    geospatial information that is desired.

    If ds_fmt is set to "auto", the function will attempt to create a cuboid,
    if the deviation between the largest and smallest interval along west_east
    and south_north are lower than value in thresh (west_east and south north
    can be different lengths). Otherwise, the function will attempt to make a
    point dataset. Specifically, it will create a 3D point object,
    if west_east, south_north and heights have the same lengths.
    If west_east and south_north have the same lengths but heights length is
    different the function will create a 2D point object.

    Alternatively, ds_fmt can be set to desired output format, that is  'cuboid',
    'stacked_point' and 'point', which accordingly requires specific structures
    of west_east, south_north and heights (as described above):

        * ``cuboid``:
            west_east, south_north, and heights must contain unique points along their
            dimension, and west_east and south_north are evenly spaced

        * ``stacked_point``:
            west_east and south_north must have the same length, but heights will have
            unique values representing the dimension values

        * ``point``:
            west_east, south_north and heights must have same lengths

    """

    # Ensure that all input arrays are 1d
    x, y, z = np.atleast_1d(west_east, south_north, height)

    if struct.lower() == "auto":
        if _has_raster_dims(x, y):
            struct = "cuboid"
        elif (y.size == x.size) and (x.size != z.size):
            struct = "stacked_point"
        elif (y.size == x.size) and (y.size == z.size):
            struct = "point"
        else:
            raise ValueError("Cannot identify struct of input data.")

    # Get names of dimensions
    x_dim, y_dim = _xy_dims()
    z_dim = _vertical_dim()
    pt_dim = _point_dim()
    stacked_pt_dim = _stacked_point_dim()

    if struct.lower() == "cuboid":
        if not _has_raster_dims(x, y):
            raise ValueError("Data cannot be converted to raster or cuboid dataset.")

        # Create spatial data arrays
        shape = z.size, y.size, x.size
        dims = (z_dim, y_dim, x_dim)
        z_coord = ((z_dim,), z)
        y_coord = ((y_dim,), y)
        x_coord = ((x_dim,), x)

    elif struct.lower() == "stacked_point":
        # Raise error if point array cannot be made
        if y.size != x.size:
            err_str = "south_north and west_east sizes do not match."
            raise ValueError(err_str)

        # Create spatial data arrays
        shape = z.size, x.size
        dims = (z_dim, stacked_pt_dim)
        z_coord = ((z_dim,), z)
        y_coord = ((stacked_pt_dim,), y)
        x_coord = ((stacked_pt_dim,), x)

    elif struct.lower() == "point":
        # Raise error if point array cannot be made
        if (y.size != x.size) | (y.size != z.size):
            err_str = (
                "point dataset cannot be made with input " + "arrays of differing sizes"
            )
            raise ValueError(err_str)

        # Create spatial data arrays
        shape = (x.size,)
        dims = (pt_dim,)
        z_coord = ((pt_dim,), z)
        y_coord = ((pt_dim,), y)
        x_coord = ((pt_dim,), x)

    else:
        raise ValueError("Unknown struct provided.")

    # Build DataArray
    data = np.zeros(shape)
    coords = {z_dim: z_coord, y_dim: y_coord, x_dim: x_coord}
    out_da = xr.DataArray(data=data, dims=dims, coords=coords)

    # Build dataset with crs for storing results
    out_ds = out_da.to_dataset(name="output")
    out_ds = add_crs(out_ds, crs)

    out_ds[z_dim].attrs = ALL_VARS_META[z_dim]
    out_ds.attrs = _GLOBAL_CONVENTIONS
    return update_history(out_ds)


def _replace_close(arr, thresh=1e-9):  # pragma:no cover internal
    """Replace all values that are close to each other with an identical value

    Parameters
    ----------
    arr : array_like
        Array to be examined
    thresh : float
        Threshold value for checking spatial separation between coordinates
        Default set to 1e-9 m


    Returns
    -------
    array_like
        Array of the same shape and dtype as arr,
        but with close values replaced
    """

    unq = np.sort(np.unique(arr))
    diff_unq = np.diff(unq)
    if any(diff_unq <= thresh):
        for i, diff in enumerate(diff_unq):
            if diff <= thresh:
                val = unq[i]
                arr = np.where(np.isclose(arr, val), val, arr)

    return arr


def reproject(obj, to_crs, copy=True):
    """Reprojects WindKit object a new CRS without changing the data.

    If the input is a xarray.Dataset or xarray.DataArray with
    a 'cuboid' spatial structure, the spatial
    structure will be changed to 'stacked_point', since the coordiates of the new
    dataset will no longer be regularly spaced.

    Parameters
    ----------
    obj : geopandas.GeoDataFrame, xarray.DataArray, xarray.Dataset, or BBox
        WindKit object that will be reprojected.
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
    copy : bool
       If true, the object is copied. Defaults to True.

    Returns
    -------
    geopandas.GeoDataFrame, xarray.DataArray,xarray.Dataset, or BBox
        WindKit object with new projection

    See Also
    --------
    warp

    Notes
    -----
    This script reprojects the coordinates of the data, and reshapes the data
    from `cuboid` or `raster` to `stacked_point`. This is done so that none of
    the data is interpolated, but rather the coordinates are just changed to match
    those of the new projection. If you want to keep your data in `cuboid` or
    `raster` format, use the function `warp` instead, which however does do
    interpolation of the data.

    """

    #
    if is_GeoDataFrame(obj) or is_GeoSeries(obj):
        return obj.to_crs(to_crs)
    elif isinstance(obj, BBox):
        return obj.reproject(to_crs)

    # From here we know that the input object is
    # a xarray.Dataset or xarray.DataArray

    if copy:
        obj = obj.copy()

    # Get input CRS object
    try:
        from_crs = get_crs(obj)
    except ValueError:
        raise ValueError(
            "No CRS found on object! Please set with:" + " obj = add_crs(obj, crs)!"
        )

    # Get spatial dim names
    x_dim, y_dim = _xy_dims()

    # Get output CRS object
    to_crs = pyproj.CRS.from_user_input(to_crs)

    # Reproject dimensions
    transformer = pyproj.Transformer.from_crs(from_crs, to_crs, always_xy=True)

    struct = get_spatial_struct(obj)

    if struct in ["raster", "cuboid"]:
        obj = to_stacked_point(obj)
        struct = "stacked_point"
    elif struct is None:
        try:
            obj = _from_scalar(obj)
            struct = get_spatial_struct(obj)
        except Exception:
            raise RuntimeError("Could not determine spatial structure of your data.")

    # Add warnings filter for numpy=1.25 from pyproj.
    # See: https://github.com/pyproj4/pyproj/issues/1307
    warnings.filterwarnings("ignore", message="Conversion of an array with ndim > 0")
    x_new, y_new = transformer.transform(obj[x_dim].values, obj[y_dim].values)
    warnings.resetwarnings()
    x_new = _replace_close(x_new)
    y_new = _replace_close(y_new)

    obj = obj.drop_vars([x_dim, y_dim])
    obj = obj.assign_coords({x_dim: ((struct), x_new), y_dim: ((struct), y_new)})

    obj = add_crs(obj, to_crs)

    return obj


def warp(
    obj, to_crs, resolution=None, method="nearest", nodata=None, coerce_to_float=True
):
    """Warp cuboid WindKit object to another in a new CRS using data interpolation.

    Parameters
    ----------
    obj : xarray.DataArray or xarray.Dataset
        WindKit object to warp.
    to_crs : int, dict, str or CRS
        Value to create CRS object or an existing CRS object
    resolution :  tuple (x resolution, y resolution) or float, optional
        Target resolution, in units of target coordinate reference
        system. Default: None calculates a resolution in the target crs similar
        to the resolution of the original crs.
    method : str
        Interpolation method, passed to rasterio.warp.reproject. Defaults to "nearest".
    nodata : scalar
        Initial data to fill output arrays, passed to rasterio.warp.reproject. Defaults to
        numpy.nan.

    Returns
    -------
    xarray.DataArray or xarray.Dataset
        Warped WindKit object.

    See Also
    --------
    reproject
    """
    kwargs = {
        "resolution": resolution,
        "method": method,
        "nodata": nodata,
        "coerce_to_float": coerce_to_float,
    }
    if isinstance(obj, (xr.Dataset, xr.DataArray)):
        struct = get_spatial_struct(obj)
        if struct in ["raster", "cuboid"]:
            obj = _warp_raster(obj, to_crs, **kwargs)
            if isinstance(obj, xr.Dataset):
                return update_history(obj)
            else:
                return obj
        else:
            raise ValueError(
                "Only 'raster' and 'cuboid' objects currently" + " supports warping!"
            )
    else:
        raise ValueError(
            "Only xarray Dataset and DataArray objects "
            + "currently supported for warping"
        )


def mask(obj, mask, all_touched=False, invert=False, nodata=None, **kwargs):
    """Mask WindKit object with geometric mask.

    Masking an object returns the same object with values outside of the masked
    region filled with NaN.

    Parameters
    ----------
    obj : xarray.Dataset,xarray.DataArray
        WindKit object to mask.
    mask : geopandas.GeoDataFrame or BBox
        Mask to mask object by.
    all_touched : bool
        *raster* or *cuboid* only: Include all pixels touched by the mask? False
        includes only those that pass through the center. Passed to
        rasterio.features.geometry_mask. Defaults to False.
    invert : bool
        *raster* or *cuboid* only: If true values outside of the mask will be nulled,
        if False values inside the mask are nulled. Opposite is passed to
        rio.features.geometry_mask. Defaults to False.
    nodata : float
        *raster* or *cuboid* only: If no data is not None, all masked data will be filled
        with this value. Default, masked data is set to NaN.

    Returns
    -------
    same as obj
        Clipped WindKit object.

    See Also
    --------
    clip

    Note
    ----
    This function behaves the opposite of rasterio.features.geometry_mask by default, in
    that it nulls areas outside of the area of interest rather than inside.
    For rasters, when the mask edges intersects with the cell centers they are not guaranteed to be
    included. It is recommend to use a buffer or all_touched=True to be sure.
    """
    kwargs = {
        **kwargs,
        "all_touched": all_touched,
        "invert": invert,
        "nodata": nodata,
    }
    if isinstance(obj, (xr.Dataset, xr.DataArray)):
        struct = get_spatial_struct(obj)
        if struct in ["raster", "cuboid"]:
            obj = _mask_raster(obj, mask, drop=False, **kwargs)
            if isinstance(obj, xr.Dataset):
                return update_history(obj)
            else:
                return obj
        elif struct in ["point", "stacked_point"]:
            obj = _mask_point(obj, mask, drop=False, **kwargs)
            if isinstance(obj, xr.Dataset):
                return update_history(obj)
            else:
                return obj
        else:
            raise ValueError("Spatial structure not supported!")
    else:
        raise ValueError("Object not supported!")


def clip(obj, mask, all_touched=False, invert=False, nodata=None, **kwargs):
    """Clip object to mask.

    Clipping returns an object that has been reduced to the requested shape. Dropping
    data that falls outside of the masked region.

    Parameters
    ----------
    obj : geopandas.GeoDataFrame, xarray.DataArray or xarray.Dataset
        Object with raster-like dimensions to clip with mask.
    mask : geopandas.GeoDataFrame or BBox
        Geometric features to clip out of object.
    all_touched : bool
        *raster* or *cuboid* only: Include all pixels touched by the mask? False
        inclodes only those that pass through the center. Passed to
        rasterio.features.geometry_mask. Defaults to False.
    invert : bool
        *raster* or *cuboid* only: If true values outside of the mask will be nulled,
        if False values inside the mask are nulled. Opposite is passed to
        rio.features.geometry_mask. Defaults to False.
    nodata : float
        *raster* or *cuboid* only: If no data is not None, all masked data will be filled
        with this value. Default, masked data is set to NaN.
    kwargs : dict
        Other keyword-arguments are passed to the underlying function, depending
        on the type of object.

    Returns
    -------
    geopandas.GeoDataFrame, xarray.DataArray,xarray.Dataset
        Object of the same type as obj clipped by geometric features.

    See Also
    --------
    mask

    Notes
    -----
    This function behaves the opposite of rasterio.features.geometry_mask by default, in
    that it nulls areas outside of the area of interest rather than inside.
    For rasters, when the mask edges intersects with the cell centers they are not guaranteed to be
    included. It is recommend to use a buffer or all_touched=True to be sure.
    """
    kwargs = {**kwargs, "all_touched": all_touched, "invert": invert, "nodata": nodata}

    if is_GeoDataFrame(obj) or is_GeoSeries(obj):
        return _clip_vector(obj, mask, **kwargs)
    elif isinstance(obj, (xr.Dataset, xr.DataArray)):
        struct = get_spatial_struct(obj)
        if struct in ["raster", "cuboid"]:
            if isinstance(mask, BBox):
                obj = _clip_to_bbox_raster(obj, mask)
            else:
                obj = _mask_raster(obj, mask, drop=True, **kwargs)
            if isinstance(obj, xr.Dataset):
                return update_history(obj)
            else:
                return obj
        elif struct in ["point", "stacked_point"]:
            obj = _mask_point(obj, mask, drop=True, **kwargs)
            if isinstance(obj, xr.Dataset):
                return update_history(obj)
            else:
                return obj
        else:
            raise ValueError("Spatial structure not supported!")
    else:
        raise ValueError(f"Object not supported!")


_STACK_ATTRS = ("_pwio_was_stacked_point", "_pwio_was_cuboid", "_pwio_orig_srs_wkt")


def spatial_stack(
    source, target_crs=None, revertable=True, copy=True, remove_height=False
):
    """Returns source in a revertable version of the "point" format

    This routine can be used to ensure a consistent input form to external routines, by
    always returning in "point" format. It can also do reprojection, and remove the
    height field to make the result a 2D spatial object.

    Parameters
    ----------
    source : xarray.DataSet
        WindKit dataset containing spatial dimensions and CRS variable to convert
    target_crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        (Default is to not reproject.)
    revertable : bool
        Should we retain information about the original datastructure so we can revert
        this process? This is typically True, but should be False when interpolating
        the data to a new projection.
    copy : bool
        Should we make a copy of the initial dataset? This is typically true as we don't
        want to manipulate the original object, but work on a new version.
    remove_height : bool
        Is the resulting object always 2D? This is typically false, but can be useful in
        some instances.

    Returns
    -------
    stacked : xarray.DataSet
        WindKit formated xr.DataSet as a point object on the new projection and
        with additional that allow it to be converted back to its original form
        using spatial_unstack.

    Notes
    -----
    This routine serves two purposes:
    1. Convert source to a point object, storing its former structure.
    2. Reproject to the target_crs if provided, and not already met.
    """
    if copy:
        source = source.copy(deep=True)

    # For some routines, we don't want to pass a height dimesion, so remove it if asked
    if remove_height:
        if has_height_dim(source):
            source = source.isel(height=0, drop=True)
        if has_height_coord(source):
            del source["height"]

    # Remove attributes from previous call if found
    if not is_point(source):
        for attr in _STACK_ATTRS:
            if attr in source.attrs:
                del source.attrs[attr]

    # Label original format and get 2D variables if not "point"
    orig_format = get_spatial_struct(source)
    if revertable and orig_format in ("stacked_point", "cuboid", "raster"):
        logger.debug("Converting from original format %s", orig_format)
        source.attrs[f"_pwio_was_{orig_format}"] = True

        if orig_format == "stacked_point":
            source.attrs["_pwio_spoint_order"] = np.lexsort(
                (source.west_east.data, source.south_north.data)
            )

        # Identify 2D variables
        if has_height_dim(source):
            hgt_dim = _vertical_dim()
            for var in source.data_vars:
                logger.debug("Flagging variable %s as 2d variable", var)
                source[var].attrs["_pwio_data_is_2d"] = hgt_dim not in source[var].dims

    # Reproject if requested
    source_crs = get_crs(source)
    if target_crs is not None:
        target_crs = pyproj.CRS.from_user_input(target_crs)
        if source_crs != target_crs:
            if revertable:
                source.attrs["_pwio_orig_srs_wkt"] = source_crs.to_wkt()
            return reproject(to_point(source), target_crs)

    ds = to_point(source)
    return update_history(ds)


def spatial_unstack(source):
    """Unstacks a point object that was created using spatial_stack

    Parameters
    ----------
    source : xarray.DataSet
        WindKit dataset containing spatial dimensions and CRS variable to revert

    Returns
    -------
    WindKit dataset
        Source dataset structured as it was originally.

    Notes
    -----
    This is the companion function to spatial_stack and does 2 things:
    1. Converts 3D-point object to either raster or 2D-point object
    2. Reprojects converted object back to its original projection
    """
    # Check that source was previously reprojected
    if "_pwio_orig_srs_wkt" in source.attrs:
        source = reproject(source, source.attrs["_pwio_orig_srs_wkt"])
        del source.attrs["_pwio_orig_srs_wkt"]

    # Convert back to original format
    if "_pwio_was_raster" in source.attrs:
        source = to_raster(source, True)
        geo_dims_order = ("south_north", "west_east")
        del source.attrs["_pwio_was_raster"]
    elif "_pwio_was_cuboid" in source.attrs:
        source = to_raster(source, True)
        geo_dims_order = ("height", "south_north", "west_east")
        del source.attrs["_pwio_was_cuboid"]
    elif "_pwio_was_stacked_point" in source.attrs:
        geo_dims_order = (
            "height",
            "stacked_point",
        )
        source = to_stacked_point(source)

        if "_pwio_spoint_order" in source.attrs:
            idx = source.attrs["_pwio_spoint_order"]
            source = source.isel(stacked_point=np.argsort(idx))
            del source.attrs["_pwio_spoint_order"]

        del source.attrs["_pwio_was_stacked_point"]

    # Transpose the coordinates to match netCDF best practices
    hgt_dim = _vertical_dim()
    if is_stacked_point(source):
        geo_dims_order = (hgt_dim,) + ("stacked_point",)
    elif is_point(source):
        geo_dims_order = ("point",)
    elif is_raster(source):
        geo_dims_order = ("south_north", "west_east")
    else:
        geo_dims_order = ("point",)

    # Removing _pwio_data_is_2d attr from dataset
    for var in source.data_vars.keys():
        if "_pwio_data_is_2d" in source[var].attrs:
            source[var].attrs.pop("_pwio_data_is_2d", None)

    ds = source.transpose(..., *geo_dims_order)
    return update_history(ds)


def nearest_points(
    ds: xr.Dataset,
    ds_target: xr.Dataset,
    dims=["west_east", "south_north", "height"],
    n_nearest=1,
    return_rank=False,
    return_distance=False,
):
    """Get nearest points from x,y,z point dataset

    Parameters
    ----------
    ds : xr.Dataset
        Input dataset of which we want to select nearest points
    ds_target : xr.Dataset
        Target dataset of the points we want to obtain from the input
    dims : list of strings
        Dimensions which we want to use for nearest neighbour lookup
    n_nearest: int
        Number of closest points to return for each point in ds_target
    return_rank: bool
        Return the rank of closeness
    return_distance: bool
        Return the distance to closest point

    Returns
    -------
    xr.Dataset
        ds but with the nearest points provided in ds_target (i.e. ds will have the shape of ds_target)
    """
    if get_crs(ds).is_geographic or get_crs(ds_target).is_geographic:
        warnings.warn(
            "You are doing nearest neighbour lookup in non metric coordinate systems!"
        )
    if get_crs(ds) != get_crs(ds_target):
        raise ValueError("Datasets must have the same coordinate system!")

    # stack so that we also work with point structure
    ds = spatial_stack(ds)

    # if we ask for only the nearest 1 point the data structure
    # remains the same as ds_target, so we can recover the original
    # by spatial_unstack.
    if n_nearest == 1:
        ds_target = spatial_stack(ds_target)
    else:
        ds_target = to_point(ds_target)

    arrays = np.array([np.atleast_1d(ds[x].values) for x in dims]).T
    arrays_target = np.array([np.atleast_1d(ds_target[x].values) for x in dims]).T
    tree = KDTree(arrays)
    dd, ii = tree.query(arrays_target, k=n_nearest)

    if n_nearest == 1:
        dims = ("point",)
    else:
        dims = ("point", "rank")

    idx = xr.DataArray(ii, dims=dims)

    nearest = ds.isel(point=idx)

    if "rank" in dims and return_rank:
        nearest["rank"] = (("rank",), np.arange(n_nearest))

    if return_distance:
        nearest["distance"] = (dims, dd)

    if n_nearest == 1:
        ds = spatial_unstack(nearest)
        return update_history(ds)
    else:
        nearest = (
            nearest.rename({"point": "point_tmp"})
            .stack(point=("point_tmp", "rank"))
            .reset_index("point")
            .drop_vars("point_tmp")
        )
        if not return_rank:
            nearest = nearest.drop_vars("rank")
        return update_history(nearest)


def covers(obj_a, obj_b):
    """
    Checks if obj_a covers obj_b

    Parameters
    ----------
    obj_a : xarray.Dataset, xarray.DataArray
        WindKit xarray dataset or dataarray containing spatial dimensions.
        Only cuboid structure is currently supported for obj_a.
    obj_b : xarray.Dataset, xarray.DataArray
        WindKit xarray dataset or dataarray containing spatial dimensions.

    Returns
    -------
    bool
        True if obj_a covers obj_b
    """

    if not is_cuboid(obj_a):
        raise ValueError(
            "obj_a must be cuboid structure, got:", get_spatial_struct(obj_a)
        )

    x_dim, y_dim = _xy_dims()
    z_dim = _vertical_dim()

    x_min, x_max = obj_a[x_dim].min(), obj_a[x_dim].max()
    y_min, y_max = obj_a[y_dim].min(), obj_a[y_dim].max()
    z_min, z_max = obj_a[z_dim].min(), obj_a[z_dim].max()

    x, y, z = obj_b[x_dim], obj_b[y_dim], obj_b[z_dim]

    return (
        (x_min <= x).all()
        & (x <= x_max).all()
        & (y_min <= y).all()
        & (y <= y_max).all()
        & (z_min <= z).all()
        & (z <= z_max).all()
    )


def clip_with_margin(
    obj_to_clip, obj_clipper, margin_dx_factor=5.0, cap_style=1, join_style=1
):
    """
    Clip a 'raster' or 'cuboid' dataset to the bounding box of another 'raster', 'cuboid', 'stacked_point',
    or 'point' dataset including a margin around that dataset to ensure several points are avaiable around
    the clipper dataset from the clipped one.

    Parameters
    ----------
    obj_to_clip : xarray Dataset or DataArray
        The dataset to clip
    obj_clipper : xarray Dataset or DataArray
        The dataset to clip to
    margin_dx_factor : float, optional
        The margin to add to the bounding box of the clipper dataset, by default 5.0,
        i.e. 5 times the grid spacing of the dataset to clip
    cap_style : int, optional
        The cap style to use for buffering the bounding box of the clipper dataset,
        by default 1 (round buffering)
    join_style : int, optional
        The join style to use for buffering the bounding box of the clipper dataset,
        by default 1 (round buffering)

    Returns
    -------
    xarray Dataset or DataArray
        The clipped dataset

    """
    obj_to_clip = obj_to_clip.copy()

    if not isinstance(obj_to_clip, (xr.Dataset, xr.DataArray)):
        raise TypeError("obj_to_clip must be an xarray Dataset or DataArray")

    if not isinstance(obj_clipper, (xr.Dataset, xr.DataArray)):
        raise TypeError("obj_clipper must be an xarray Dataset or DataArray")

    if not is_raster(obj_to_clip):
        raise ValueError("obj_to_clip must be a cuboid")

    # Get the CRS of the dataset to clip and the grid spacing resolution
    # to use for buffering of the bounding buffer
    # (5 times the resolution of the climate dataset)
    # We will use the bbox to clip the climate dataset before interpolation
    crs_clip = get_crs(obj_to_clip)
    spacing_clip, _ = _raster_resolution(obj_to_clip)
    bbox_buffer = margin_dx_factor * spacing_clip

    # Create a bounding box around the output locations buffered with enough edge points
    # for the interpolation to work¨
    # cap_style=1, join_style=1 is used (round buffering) to avoid issues with
    # spatial datasets of points forming a straigth line (default buffer is square
    # and wont buffer the points in this case)
    bbox = (
        BBox.from_ds(obj_clipper)
        .reproject(crs_clip)
        .buffer(bbox_buffer, cap_style=cap_style, join_style=join_style)
        .envelope()
    )

    # check if bbox is outside bounds of the dataset
    bounds_to_clip = _raster_bounds(obj_to_clip)
    bounds_bbox = bbox.bounds()
    if (
        bounds_bbox[0] < bounds_to_clip[0]
        or bounds_bbox[1] < bounds_to_clip[1]
        or bounds_bbox[2] > bounds_to_clip[2]
        or bounds_bbox[3] > bounds_to_clip[3]
    ):
        warnings.warn(
            "Clipping bbox including marging is outside the bounds of the dataset to clip!"
        )

    # Clip the dataset to the bounding box
    return clip(obj_to_clip, bbox)


def equal_spatial_shape(obj_a, obj_b):
    """Check if two spatial objects have the same shape.

    Parameters
    ----------
    obj_a : xr.Dataset or xr.DataArray
        Spatial object.
    obj_b : xr.Dataset or xr.DataArray
        Spatial object.

    Returns
    -------
    bool
        True if the objects have the same shape, False otherwise.
    """
    struct_a = get_spatial_struct(obj_a)
    struct_b = get_spatial_struct(obj_b)

    if struct_a != struct_b:
        return False

    if struct_a == "point":
        return obj_a.point.size == obj_b.point.size
    elif struct_a == "stacked_point":
        return (
            obj_a.stacked_point.size == obj_b.stacked_point.size
            and obj_a.height.size == obj_b.height.size
        )
    elif struct_a == "cuboid":
        return (
            obj_a.west_east.size == obj_b.west_east.size
            and obj_a.south_north.size == obj_b.south_north.size
            and obj_a.height.size == obj_b.height.size
        )
    elif struct_a == "raster":
        return (
            obj_a.west_east.size == obj_b.west_east.size
            and obj_a.south_north.size == obj_b.south_north.size
        )
    else:
        raise ValueError(f"Unknown spatial structure '{struct_a}'.")


def ds_to_gdf(ds, include_height=False):
    """Convert windkit spatial structure to geopandas dataframe.

    Parameters
    ----------
    ds : xr.Dataset or xr.DataArray
        Spatial object.
    include_height : boolean, optional
        Default False, do not include the height dimension in the geopandas dataframe

    Returns
    -------
    gdf : gpd.GeoDataFrame
        GeoDataFrame with columns `x`, `y` and optionally `z` if include_height is True

    Notes
    -----
    If a coordinate `name` is present on the dataset, it will be included
    in the geodataframe as well. This can be convenient when you have mast
    locations that have a name/label. Note that if your dataset is in cuboid
    or stacked_point format, it will be flattened to a point structure.
    """
    gpd = requires_geopandas()

    point_ds = to_point(ds)
    in_crs = get_crs(ds)
    struct = (point_ds.coords["west_east"], point_ds.coords["south_north"])
    if include_height:
        struct = struct + (point_ds.coords["height"],)
    try:
        gdf = gpd.GeoDataFrame(
            {"name": point_ds["name"]}, geometry=gpd.points_from_xy(*struct), crs=in_crs
        )
    except:
        gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(*struct), crs=in_crs)

    return gdf.drop_duplicates()


def _get_coords_from_gdf(gdf, height=None):
    """
    Extracts the x, y, and z coordinates from a GeoDataFrame. If the GeoDataFrame
    does not contain z values, a specified height is used for all points.

    Parameters
    ----------
    gdf : GeoDataFrame
        The GeoDataFrame from which to extract the coordinates. The GeoDataFrame
        should contain a 'geometry' column with Point geometries. If the points
        do not have a z coordinate, the 'height' parameter must be provided.
    height : float or None
        The height to use for all points if the GeoDataFrame does not contain
        z values. If the GeoDataFrame does contain z values, this parameter is
        ignored. If the GeoDataFrame does not contain z values and this parameter
        is None, a ValueError is raised.

    Returns
    -------
    x, y, z : ndarray
        The x, y, and z coordinates of the points in the GeoDataFrame. The
        coordinates are returned as separate 1D numpy arrays.

    Raises
    ------
    ValueError
        If the GeoDataFrame does not contain z values and 'height' is None.
    """
    if all(gdf.geometry.has_z):
        x, y, z = gdf.geometry.get_coordinates(include_z=True).values.T
    else:
        x, y = gdf.geometry.get_coordinates(include_z=False).values.T
        if height is None:
            raise ValueError(
                "You must provide a height for the dataset, because the geodataframe only contains x and y!"
            )
        z = np.full_like(x, height)
    return x, y, z


def gdf_to_ds(gdf, height=None, struct=None):
    """Convert geopandas dataframe to windkit spatial structure.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        Geopandas dataframe with geometry column
    height : float, optional
        The value of the height coordinate if it is not included in the gpd.GeoDataFrame.
    struct : {"point", "stacked_point", "cuboid"}
        Default None, which means detect the best fitting windkit spatial structure.

    Returns
    -------
    ds : xr.Dataset
        dataset with a windkit spatial structure.

    Notes
    -----
    If a column `name` is present on the GeoDataFrame and your data is
    in point or stacked_point structure, it will be included in the xr.Dataset as well.
    This can be convenient when you have mast locations that have a name/label.
    """
    x, y, z = _get_coords_from_gdf(gdf, height=height)

    if struct is None:
        x, y, z = np.unique(x), np.unique(y), np.unique(z)
        # check if dataset can be a raster
        if _can_be_raster(x, y):
            struct = "cuboid"
            # in horizontal plane we can have a cuboid, but height dimension is varying, so return point
            if np.mod(gdf.size, z.size) != 0:
                struct = "point"
                x, y, z = _get_coords_from_gdf(gdf, height=height)
        elif np.mod(gdf.size, z.size) == 0:
            struct = "stacked_point"
        else:
            struct = "point"

    ds = create_dataset(x, y, z, struct=struct, crs=gdf.crs)

    if "name" in gdf.columns and (struct == "point" or struct == "stacked_point"):
        if struct == "stacked_point":
            if gdf["name"].unique().size != x.size:
                raise ValueError("Name must be unique for each stacked point.")
            names = gdf["name"].unique()
        else:
            names = gdf["name"]
        ds.coords["name"] = (struct, names)

    return ds
