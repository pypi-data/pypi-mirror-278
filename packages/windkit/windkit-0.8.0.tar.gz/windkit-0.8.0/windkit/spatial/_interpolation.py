"""Internal interpolation routines

These routines are used to resample and reproject the source data to target grid
"""
import warnings

import numpy as np
import scipy.interpolate
import xarray as xr
from scipy.spatial import Delaunay

from ..metadata import update_history
from . import _metpy_natural_neighbors as metpy_nn
from .spatial import (
    are_spatially_equal,
    crs_are_equal,
    get_crs,
    is_cuboid,
    is_point,
    is_raster,
    is_stacked_point,
    spatial_stack,
    to_point,
    to_raster,
)

SPATIAL_COORDS = ["height", "south_north", "west_east"]
HORIZONTAL_COORDS = ["south_north", "west_east"]
NUMERIC_DTYPE_KINDS = "fiuc"
NONNUMERIC_DTYPE_KINDS = "mMOSUV"


def interp_structured_like(source, target, exclude_dims=None, **kwargs):
    """
    Interpolate spatially from cuboid dataset/dataarray to another spatial dataset/dataarray

    Parameters
    ----------
    source : xarray.Dataset or xarray.DataArray
        Source dataset/dataarray with spatial coordinates. Must be a cuboid and have
        the same crs as target.

    target : xarray.Dataset or xarray.DataArray
        Target dataset/dataarray with spatial coordinates. Can be a cuboid, stacked_point or point.
        Must have the same crs as source.

    exclude_dims : list, optional
        List of dimensions to exclude from interpolation. Default is None

    Returns
    -------
    xarray.Dataset or xarray.DataArray
        Interpolated dataset/dataarray with spatial coordinates of target

    Raises
    ------
    ValueError
        If source and target are not xarray.Dataset or xarray.DataArray

    ValueError
        If source and target do not have the same crs

    Warnings
    --------
    If any of the variables in source are not numeric, they will be skipped and a warning will be raised.

    """

    if not isinstance(source, (xr.Dataset, xr.DataArray)):
        raise ValueError(
            "source must be an xarray.Dataset or xarray.DataArray. Got {}".format(
                type(source)
            )
        )

    if not isinstance(target, (xr.Dataset, xr.DataArray)):
        raise ValueError(
            "target must be an xarray.Dataset or xarray.DataArray. Got {}".format(
                type(target)
            )
        )

    if isinstance(source, xr.Dataset):
        if any(
            source[v].dtype.kind not in NUMERIC_DTYPE_KINDS for v in source.data_vars
        ):
            warnings.warn(
                "Skipping interpolation of non-numeric variables. "
                + "Only numeric variables are interpolated.",
                UserWarning,
            )
            source = source[
                [
                    v
                    for v in source.data_vars
                    if source[v].dtype.kind in NUMERIC_DTYPE_KINDS
                ]
            ]
    else:  # can only be a DataArray at this point.
        if source.dtype.kind not in NUMERIC_DTYPE_KINDS:
            raise ValueError(
                "source must be numeric. Got dtype {}".format(source.dtype)
            )

    if not crs_are_equal(source, target):
        raise ValueError(
            "source and target must have the same crs. Got {} and {}".format(
                source.crs, target.crs
            )
        )

    if not (is_cuboid(source) or is_raster(source)):
        raise ValueError("source must be a cuboid or raster. Got {}".format(source))

    if exclude_dims is None:
        exclude_dims = []

    coords_kwargs = {
        k: v
        for k, v in target.coords.items()
        if (k in SPATIAL_COORDS and k in source.coords and k not in exclude_dims)
    }

    return source.interp(**coords_kwargs, **kwargs)


def _interp_unstructured_da(
    obj, west_east=None, south_north=None, height=None, method="linear", **kwargs
):
    """
    Interpolate spatially from unstructured dataset/dataarray to new coordinates

    Parameters
    ----------
    obj : xarray.DataArray
        Source dataarray with spatial coordinates. Can be a cuboid, stacked_point or point.
        Must have the same crs as the west_east, south_north and height coordinates provided.

    west_east : xarray.DataArray, optional
        Target dataarray with spatial coordinates.
        Can be in cuboid, stacked_point or point structure

    south_north : xarray.DataArray, optional
        Target dataarray with spatial coordinates.
        Can be in cuboid, stacked_point or point structure

    height : xarray.DataArray, optional
        Target dataarray with spatial coordinates.
        Can be in cuboid, stacked_point or point structure

    method : str, optional
        Interpolation method. Must be 'nearest', 'linear', or 'cubic'. Default is 'linear'

    **kwargs : dict
        Keyword arguments passed to interpolation function

    Returns
    -------
    xarray.DataArray
        Interpolated dataarray with spatial coordinates of target

    Raises
    ------
    ValueError
        If obj is not an xarray.DataArray

    ValueError
        If any of the coordinates in coords_kwargs are not xarray.DataArray

    ValueError
        If any of the coordinates in coords_kwargs are not in obj

    Warnings
    --------
    If obj is not numeric, it will be skipped and a warning will be raised.

    """

    if not isinstance(obj, xr.DataArray):
        raise ValueError("obj must be an xarray.DataArray. Got {}".format(type(obj)))

    coords_kwargs = {
        name: coord
        for name, coord in zip(SPATIAL_COORDS, [height, south_north, west_east])
        if coord is not None
    }

    if not all(isinstance(coord, xr.DataArray) for coord in coords_kwargs.values()):
        raise ValueError(
            "All coordinates in coords_kwargs must be xarray.DataArray. Got {}".format(
                [type(coord) for coord in coords_kwargs.values()]
            )
        )

    if not "point" in obj.dims:
        stack_dims = []
        if "height" in coords_kwargs and "height" in obj.dims:
            stack_dims.append("height")

        if "stacked_point" in obj.dims:
            if any(c in coords_kwargs for c in HORIZONTAL_COORDS):
                stack_dims += ["stacked_point"]

        if all((c in coords_kwargs and c in obj.dims) for c in HORIZONTAL_COORDS):
            stack_dims += HORIZONTAL_COORDS

        if len(stack_dims) > 0:
            obj = obj.stack(__point__=stack_dims)
    else:
        obj = obj.rename({"point": "__point__"})

    if any(c not in obj.coords for c in coords_kwargs.keys()):
        raise ValueError(
            "All dimensions in coords_kwargs must be in obj. Got {}.".format(
                coords_kwargs.keys()
            )
        )

    coords_interp = coords_kwargs.keys()
    points = np.array(tuple(obj[coord] for coord in coords_interp)).T

    points_new = tuple(coords_kwargs[dim] for dim in coords_interp)
    points_new = xr.broadcast(*points_new)
    dims_result = points_new[0].dims

    n_coords_interp = len(coords_interp)
    n_dims_interp = points_new[0].ndim

    if n_coords_interp == 1:

        def _interp(arr):
            return scipy.interpolate.griddata(
                points, arr, points_new, method=method, **kwargs
            )

    else:
        if method == "cubic":
            if n_dims_interp > 2:
                raise ValueError(
                    "cubic interpolation only supported for 2D interpolation. Got {} dims".format(
                        n_dims_interp
                    )
                )
            interp_func = scipy.interpolate.CloughTocher2DInterpolator
        elif method == "linear":
            interp_func = scipy.interpolate.LinearNDInterpolator
        elif method == "nearest":
            interp_func = scipy.interpolate.NearestNDInterpolator
        else:
            raise ValueError(
                "method must be 'nearest', 'linear', or 'cubic'. Got {}".format(method)
            )

        if method != "nearest":
            x = Delaunay(points)
        else:
            x = points

        def _interp(arr):
            interpolator = interp_func(x, arr, **kwargs)
            return interpolator(points_new)

    result = xr.apply_ufunc(
        _interp,
        obj,
        input_core_dims=[["__point__"]],
        output_core_dims=[dims_result],
        vectorize=True,
    )

    result = result.assign_coords(**coords_kwargs)

    return result


def _interp_unstructured_natural_neighbor(obj, west_east, south_north):
    """
    Interpolate unstructured spatial data using natural neighbor interpolation.

    Parameters
    ----------
    obj : xarray.Dataset or xarray.DataArray
        Source dataset/dataarray with spatial coordinates. Must be in 'point' structure.
        Must have the same crs as the west_east and south_north coordinates provided.

    west_east : xarray.DataArray
        Target dataarray with west_east coordinates.
        Must be in 'point' structure

    south_north : xarray.DataArray
        Target dataarray with south_north coordinates.
        Must be in 'point' structure

    **kwargs : dict

    Returns
    -------
    xarray.Dataset or xarray.DataArray
        Interpolated dataset/dataarray with spatial coordinates of target

    Raises
    ------
    ValueError
        If obj is not an xarray.Dataset or xarray.DataArray

    ValueError
        If obj is not in 'point' structure

    ValueError
        If west_east or south_north are not xarray.DataArray

    ValueError
        If west_east or south_north are not in 'point' structure

    Warnings
    --------
    If any of the variables in obj are not numeric, they will be skipped and a warning will be raised.

    """

    if west_east is None or south_north is None:
        raise ValueError(
            "west_east and south_north must be provided for natural_neighbor interpolation"
        )

    if not all(is_point(c) for c in [west_east, south_north]):
        raise ValueError(
            "west_east and south_north must be in point structure for natural_neighbor interpolation"
        )

    if not west_east.ndim == south_north.ndim == 1:
        raise ValueError(
            "west_east and south_north must be 1D (point structure) for natural_neighbor interpolation"
        )

    if isinstance(obj, xr.Dataset):
        if any(obj[v].dtype.kind not in NUMERIC_DTYPE_KINDS for v in obj.data_vars):
            warnings.warn(
                "Skipping interpolation of non-numeric variables. "
                + "Only numeric variables are interpolated.",
                UserWarning,
            )
            obj = obj[
                [v for v in obj.data_vars if obj[v].dtype.kind in NUMERIC_DTYPE_KINDS]
            ]

    xy_coords = ["west_east", "south_north"]
    if not is_point(obj):
        obj = obj.stack(__point__=xy_coords)
    else:
        obj = obj.rename({"point": "__point__"})

    points = np.array(tuple(obj[coord] for coord in xy_coords)).T
    points_new = np.array(tuple([west_east, south_north])).T

    tri = Delaunay(points)
    in_triangulation = tri.find_simplex(points_new) >= 0

    match = np.array([(pt == points).all(axis=1).any() for pt in points_new])
    nomatch = np.logical_not(match)

    use_natural = np.logical_and(in_triangulation, nomatch)
    use_nearest = np.logical_or(np.logical_not(in_triangulation), match)

    if isinstance(obj, xr.DataArray):

        def _interp(arr):
            arr_out = np.empty(points_new.shape[0])
            arr_out[use_natural] = metpy_nn.natural_neighbor_to_points(
                points, arr, points_new[use_natural]
            )
            arr_out[use_nearest] = scipy.interolate.griddata(
                points, arr, points_new[use_nearest], method="nearest"
            )
            return arr_out

    elif isinstance(obj, xr.Dataset):
        neighbors_list, weights_list = metpy_nn.find_all_neighbors_and_weights(
            points, points_new[use_natural]
        )

        def _interp(arr):
            arr_out = np.empty(points_new.shape[0])

            arr_out[use_natural] = metpy_nn.interpolate_natural_neighbors(
                points, arr, points_new[use_natural], neighbors_list, weights_list
            )
            arr_out[use_nearest] = scipy.interpolate.griddata(
                points, arr, points_new[use_nearest], method="nearest"
            )
            return arr_out

    result = xr.apply_ufunc(
        _interp,
        obj,
        input_core_dims=[["__point__"]],
        output_core_dims=[["point"]],
        vectorize=True,
        keep_attrs=True,
    )

    result = result.assign_coords(
        {
            "west_east": west_east,
            "south_north": south_north,
        }
    )

    return result


def interp_unstructured(
    obj, west_east=None, south_north=None, height=None, method="linear", **kwargs
):
    """
    Interpolate spatially from unstructured dataset/dataarray to new coordinates.

    Parameters
    ----------
    obj : xarray.Dataset or xarray.DataArray
        Source dataset/dataarray with spatial coordinates. Can be a cuboid, stacked_point or point.
        Must have the same crs as the west_east, south_north and height coordinates provided.

    west_east : xarray.DataArray, optional
        Target dataarray with spatial coordinates.
        Can be in cuboid, stacked_point or point structure

    south_north : xarray.DataArray, optional
        Target dataarray with spatial coordinates.
        Can be in cuboid, stacked_point or point structure

    height : xarray.DataArray, optional
        Target dataarray with spatial coordinates.
        Can be in cuboid, stacked_point or point structure

    method : str, optional
        Interpolation method. Must be 'nearest', 'linear',  'cubic', or 'natural. Default is 'linear'

    **kwargs : dict
        Keyword arguments passed to interpolation function

    Returns
    -------
    xarray.Dataset or xarray.DataArray
        Interpolated dataset/dataarray with spatial coordinates provided.

    Raises
    ------
    ValueError
        If obj is not an xarray.Dataset or xarray.DataArray

    ValueError
        If any of the coordinates in coords_kwargs are not xarray.DataArray

    ValueError
        If any of the coordinates in coords_kwargs are not in obj

    Warnings
    --------
    If any of the variables in obj are not numeric, they will be skipped and a warning will be raised.

    """

    if not isinstance(obj, (xr.DataArray, xr.Dataset)):
        raise ValueError(
            "obj must be an xarray.Dataset or xarray.DataArray. Got {}".format(
                type(obj)
            )
        )

    # Spatial case for natural neighbor interpolation
    if method == "natural":
        return _interp_unstructured_natural_neighbor(
            obj, west_east, south_north, **kwargs
        )

    coords_kwargs = {
        name: coord
        for name, coord in zip(SPATIAL_COORDS, [height, south_north, west_east])
        if coord is not None
    }

    if isinstance(obj, xr.DataArray):
        return _interp_unstructured_da(
            obj,
            west_east=west_east,
            south_north=south_north,
            height=height,
            method=method,
            **kwargs,
        )

    results = []
    for var in obj.data_vars:
        coords_kwargs_da = {
            k: v for k, v in coords_kwargs.items() if k in obj[var].coords
        }

        if len(coords_kwargs_da.keys()) == 0:
            results.append(obj[var])
            continue

        if obj[var].dtype.kind not in NUMERIC_DTYPE_KINDS:
            warnings.warn(
                "Skipping interpolation of {}. Not a numeric type.".format(var),
                UserWarning,
            )
            continue

        results.append(
            _interp_unstructured_da(
                obj[var], **coords_kwargs_da, method=method, **kwargs
            )
        )

    ds = xr.merge(results)

    return ds


def interp_unstructured_like(source, target, exclude_dims=None, **kwargs):
    """
    Interpolate spatially from unstructured dataset/dataarray to another spatial dataset/dataarray

    Parameters
    ----------
    source : xarray.Dataset or xarray.DataArray
        Source dataset/dataarray with spatial coordinates. Can be a cuboid, stacked_point or point.
        Must have the same crs as target.

    target : xarray.Dataset or xarray.DataArray
        Target dataset/dataarray with spatial coordinates. Can be a cuboid, stacked_point or point.
        Must have the same crs as source.

    exclude_dims : list, optional
        List of dimensions to exclude from interpolation. Default is None

    **kwargs : dict
        Keyword arguments passed to scipy.interpolate.griddata

    Returns
    -------
    xarray.Dataset or xarray.DataArray
        Interpolated dataset/dataarray with spatial coordinates of target

    Raises
    ------
    ValueError
        If source and target are not xarray.Dataset or xarray.DataArray

    ValueError
        If source and target do not have the same crs

    """

    if not isinstance(source, (xr.DataArray, xr.Dataset)):
        raise ValueError(
            "source must be an xarray.Dataset or xarray.DataArray. Got {}".format(
                type(source)
            )
        )

    if not isinstance(target, (xr.DataArray, xr.Dataset)):
        raise ValueError(
            "target must be an xarray.Dataset or xarray.DataArray. Got {}".format(
                type(target)
            )
        )

    if not crs_are_equal(source, target):
        raise ValueError(
            "source and target must have the same crs. Got {} and {}".format(
                source.crs, target.crs
            )
        )

    if exclude_dims is None:
        exclude_dims = []

    coords_kwargs = {
        k: v
        for k, v in target.coords.items()
        if (k in SPATIAL_COORDS and k in source.coords and k not in exclude_dims)
    }
    return interp_unstructured(source, **coords_kwargs, **kwargs)


def _single_pt(source, target, exclude=True):  # pragma: no cover
    """Broadcast source single point dataset to all points in target dataset

    Parameters
    ----------
    source : xarray.Dataset
        PyWAsP 3D point dataset
    target : xarray.Dataset
        PyWAsP xr.DataSet

    Returns
    -------
    xarray.Dataset
        Broadcasted source xr.DataSet

    Raises
    ------
    ValueError
        If source xr.DataSet contains more than a single point
    """
    if exclude:
        raise ValueError(
            "Single point data provided, but single-point interpolation excluded."
        )
    if source.sizes["point"] != 1:
        raise ValueError("Can only project to a single point if point dimension == 1.")
    # Convert target to points
    out_pts = to_point(target)

    # Broadcast the data to all of the points
    out = xr.broadcast(source.squeeze("point"), out_pts, exclude=source.CORE_DIMS)[0]
    out["west_east"] = out_pts.west_east
    out["south_north"] = out_pts.south_north
    out["height"] = out_pts.height

    # Return to raster if target was raster
    if is_raster(target):
        out = to_raster(out)

    return out


def _nearest(source, target):  # pragma: no cover
    """Nearest neighbor interpolation of source point dataset to target grid

    Parameters
    ----------
    source: xarray.Dataset
        PyWAsP 3D point dataset
    target: xarray.Dataset
        PyWAsP 3D point dataset
    """
    # Create a 3D tuple of the input points
    points = (source.west_east, source.south_north, source.height)

    # Combine all of the output points into a tuple
    if is_raster(target):
        out_mesh_x, out_mesh_y, out_mesh_z = np.meshgrid(
            target.west_east, target.south_north, target.height
        )
        xi = (out_mesh_x, out_mesh_y, out_mesh_z)
    else:
        xi = (target.west_east, target.south_north, target.height)

    # Get indices of the nearest point
    idx = scipy.interpolate.griddata(
        points, np.arange(source["point"].size), xi, method="nearest"
    )

    # Subset and reshape array
    out = source.isel(point=idx.flatten().astype("int"))

    # Reshape to raster if necessary
    if is_raster(target):
        # Set new coordinate values to match the target coorinates
        out.coords["west_east"].values = xi[0].flatten()
        out.coords["south_north"].values = xi[1].flatten()
        out.coords["height"].values = xi[2].flatten()
        out = to_raster(out)
    else:
        # Set new coordinate values to match the target coorinates
        out.coords["west_east"].values = xi[0].values
        out.coords["south_north"].values = xi[1].values
        out.coords["height"].values = xi[2].values

    return out


def interpolate_to_grid(source, target, method, exclude=False):  # pragma: no cover
    """Resamples source to target grid

    Parameters
    ----------
    source : xarray.Dataset
        PyWAsP 3D point dataset with geographic coordinates and crs
    target : xarray.Dataset
        PyWAsP dataset with geographic coordinates and crs
    method : string
        Method of interpolation, currently only nearest is supported
    exclude: bool, optional
        To exclude _single_pt interpolation method, by default False

    Returns
    -------
    xr.Dataset
        Source dataset interpolated to the target grid

    Raises
    ------
    ValueError
        If source and target grids are different
    """
    warnings.warn(
        "The 'interpolate_to_grid' function is deprecated and will be removed in a future version. "
        + "Use 'interp_structured_like' or 'interp_unstructured_like' instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    target_crs = get_crs(target.crs)
    source = spatial_stack(source, target_crs, False)

    # Need to always have a height column, so add it if there isn't a height coord
    if "height" not in source.coords:
        source.coords["height"] = xr.DataArray(
            np.repeat([10], source.sizes["point"]), dims=["point"]
        )
        for var in source.data_vars:
            source[var].attrs["_pwio_data_is_2d"] = False

    # Only single point and nearest are setup right now
    if source.sizes["point"] == 1:
        res = _single_pt(source, target, exclude)
        return update_history(res)

    if method == "nearest":
        res = _nearest(source, target)
        return res

    if not are_spatially_equal(to_point(source), to_point(target)):
        raise ValueError(
            "source and target grids are different, "
            + "so you need to specify an interpolation method."
        )
    return update_history(source)
