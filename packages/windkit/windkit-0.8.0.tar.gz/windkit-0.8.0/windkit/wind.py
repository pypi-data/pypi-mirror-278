# (c) 2022 DTU Wind Energy
"""
Utility functions for working with wind data
"""
import numpy as np
import pandas as pd
import xarray as xr
from scipy.integrate import trapezoid

from windkit.sector import create_sector_coords, create_sector_coords_from_edges


def wind_speed(u, v):
    """
    Calculate wind speed from wind vectors.

    Parameters
    ----------
    u, v : numpy.ndarray, xarray.DataArray
        U and V wind vectors.

    Returns
    -------
    ws : numpy.ndarray, xarray.DataArray
        Wind speed.

    """
    return np.sqrt(u * u + v * v)


def wind_direction(u, v):
    """
    Calculate wind directions from wind vectors.

    Parameters
    ----------
    u, v : np.ndarray, xr.DataArray
        U and V wind vectors.

    Returns
    -------
    wd : np.ndarray, xr.DataArray
        Wind direction

    """
    return 180.0 + np.arctan2(u, v) * 180.0 / np.pi


def wind_speed_and_direction(u, v):
    """
    Calculate wind speed and wind direction from wind vectors.

    Parameters
    ----------
    u, v : numpy.ndarray, xarray.DataArray
        U and V wind vectors.

    Returns
    -------
    speed : numpy.ndarray, xarray.DataArray
        Wind speed.
    direction : numpy.ndarray, xarray.DataArray
        Wind direction.

    """
    return wind_speed(u, v), wind_direction(u, v)


def wind_vectors(ws, wd):
    """
    Calculate wind vectors u,v from the speed and direction.

    Parameters
    ----------
    speed : numpy.ndarray, xarray.DataArray
        Wind speed
    direction : numpy.ndarray, xarray.DataArray
        Wind direction

    Returns
    -------
    u, v : numpy.ndarray, xarray.DataArray
        Wind vectors u and v

    """
    return (
        -np.abs(ws) * np.sin(np.pi / 180.0 * wd),
        -np.abs(ws) * np.cos(np.pi / 180.0 * wd),
    )


def wind_direction_difference(wd_obs, wd_mod):
    """
    Calculate the circular (minimum) distance between
    two directions (observed and modelled).

    Parameters
    ----------
    wd_obs : xarray.DataArray
        observed direction arrays.
    wd_mod: xarray.DataArray
        modelled direction arrays.

    Returns
    -------
    xarray.DataArray: circular (minimum) differences.

    Examples
    --------
    >>> wd_obs = xr.DataArray([15.0, 345.0, 355.0], dims=('time',))
    >>> wd_mod = xr.DataArray([345.0, 300.0, 5.0], dims=('time',))
    >>> wind_direction_difference(wd_obs, wd_mod)
    <xarray.DataArray (time: 3)>
    array([-30., -45.,  10.])
    Dimensions without coordinates: time

    """
    wd_diff = wd_mod - wd_obs
    wd_diff = wd_diff.where(wd_diff < 180.0, wd_diff - 360.0)
    wd_diff = wd_diff.where(wd_diff > -180.0, wd_diff + 360.0)
    return wd_diff


def wd_to_sector(wd, bins=12, output_type="centers", quantiles=False):
    """
    Convert wind directions to 0-based sector indices.

    Parameters
    ----------
    wd : xarray.DataArray, numpy.array
        Wind directions. The function uses xarray.apply_ufunc, so the return value
        will keep the shape of the input value.
    bins : int
        Number of bins / sectors. Defaults to 12.
    output_type : str
        If set to 'centers' the values in 'wd' are the sector centers. If set to
        'indices', the values in 'wd' are the sector indices. Defaults to 'centers'.
    quantiles : bool
        Allows to use equal probability sectors (quantiles=True) instead of fixed
        width sectors. Note that this is an experimental feature to be used only
        together with the `widkit.mcp` module for now. Other `windkit` modules may
        not be compatible with non fixed width sectors. Defaults to False.
    Returns
    -------
    sectors :  xarray.DataArray,np.array
        wind speed sector centers.
    sector_coords : xarray.DataArray
        data array with sector coordinates incling center, ceiling and floor.

    Examples
    --------
    >>> wd = xr.DataArray([355.0, 14.0, 25.0, 270.0,], dims=('time',))
    >>> wd_to_sector(wd)
    (<xarray.DataArray (time: 4)>
    array([  0.,   0.,  30., 270.])
    Dimensions without coordinates: time,
    <xarray.DataArray (sector: 12)>
    array([  0.,  30.,  60.,  90., 120., 150., 180., 210., 240., 270., 300.,
        330.])
    Coordinates:
      * sector        (sector) float64 0.0 30.0 60.0 90.0 ... 270.0 300.0 330.0
        sector_ceil   (sector) float64 15.0 45.0 75.0 105.0 ... 285.0 315.0 345.0
        sector_floor  (sector) float64 345.0 15.0 45.0 75.0 ... 255.0 285.0 315.0)
    """

    def _wd_to_sector_constant(wd, bins=12):
        width = 360.0 / bins
        edges = np.linspace(0.0, 360.0, bins + 1)
        edges[0] = -0.1
        edges[-1] = 360.1
        sector = np.digitize(np.mod(wd + width / 2.0, 360.0), edges) - 1
        sector = sector.astype(np.float64)
        sector[sector >= bins] = np.nan
        return sector

    def _wd_to_sector_quantiles(wd, bins=12):
        # TODO move this to xarray nor numpy so we can use apply_ufunc
        sector_da = wd.copy()
        sector_cat, edges = pd.qcut(wd.values.flatten(), bins, retbins=True)
        edges[0] = 0.0
        edges[-1] = 360.0
        sector_da.data = sector_cat.codes.reshape(wd.shape)
        sector_coords_da = create_sector_coords_from_edges(edges)
        return sector_da, sector_coords_da

    if output_type not in ["centers", "indices"]:
        raise ValueError("unkown output type. Possible values are 'centers','indices'")

    if not quantiles:
        sectors = xr.apply_ufunc(_wd_to_sector_constant, wd, kwargs={"bins": bins})
        sector_coords = create_sector_coords(bins)
        centers = sectors * 360.0 / bins

    else:
        if (
            type(wd) is not xr.DataArray
            or ("point" not in wd.dims)
            or (len(wd["point"]) > 1)
        ):
            raise ValueError(
                "For quantiles=True, only xarray.DataArray with point dimensions of length 1 are supported"
            )
        sectors, sector_coords = _wd_to_sector_quantiles(wd, bins)
        centers_values = sector_coords.isel(sector=sectors.values.flatten()).values
        centers = wd.copy()
        centers.values = centers_values.reshape(-1, 1)

    if output_type == "indices":
        return sectors, sector_coords
    else:
        return centers, sector_coords


def vinterp_wind_direction(wind_direction, height, **kwargs):
    """
    Interpolate wind direction to a given height.

    Parameters
    ----------
    wind_direction : xarray.DataArray
        Wind direction.
    height : float
        Height to interpolate wind direction to.
    **kwargs : dict, optional
        Additional keyword arguments passed to xarray.interp.

    Returns
    -------
    wind_direction : xarray.DataArray
        Interpolated wind direction.

    """
    if not isinstance(wind_direction, xr.DataArray):
        raise TypeError("wind_direction must be a xarray.DataArray")

    if "height" not in wind_direction.dims:
        raise ValueError("wind_direction must have a height dimension")

    if not isinstance(height, (np.ScalarType, xr.DataArray)):
        raise TypeError("height must be a scalar or xarray.DataArray")

    wd_ref = wind_direction.isel(height=0)
    wd_diff = wind_direction_difference(wind_direction, wd_ref)
    wd_new = wd_ref - wd_diff.interp(height=height, **kwargs)
    return np.mod(wd_new, 360.0)


def vinterp_wind_speed(wind_speed, height, log_height=True, **kwargs):
    """
    Vertically interpolate wind speed to a given height from other height levels.

    Parameters
    ----------
    wind_speed : xarray.DataArray
        Wind speed. Must have a height dimension.
    height : float, xarray.DataArray
        Height to interpolate wind speed to.
    log_height : bool, optional
        If True, interpolate in log-height space. Defaults to True.
    **kwargs : dict, optional
        Additional keyword arguments passed to xarray.interp.

    Returns
    -------
    wind_speed : xarray.DataArray
        Interpolated wind speed.

    """

    if not isinstance(wind_speed, xr.DataArray):
        raise TypeError("wind_speed must be a xarray.DataArray")

    if "height" not in wind_speed.dims:
        raise ValueError("wind_speed must have a height dimension")

    if not isinstance(height, (np.ScalarType, xr.DataArray)):
        raise TypeError("height must be a scalar or xarray.DataArray")

    wind_speed = wind_speed.copy()

    if log_height:
        wind_speed = wind_speed.assign_coords(height=np.log1p(wind_speed.height))
        if isinstance(height, xr.DataArray):
            height_ = height.copy()
        height = np.log1p(height)

    wind_speed = wind_speed.interp(height=height, **kwargs)

    if log_height and isinstance(height_, xr.DataArray):
        wind_speed = wind_speed.assign_coords(height=height_)

    return wind_speed


def rotor_equivalent_wind_speed(
    wind_speed,
    wind_direction,
    hub_height,
    rotor_diameter,
    delta_z=1.0,
    n_integrate=1001,
):
    """
    Calculate the rotor equivalent wind speed (REWS) from given wind speed and directions
    on height levels.

    The procedure is as follows:
        1. Find the area of each segment of the rotor spanned area.
        2. Calculate the wind speed at the center of each segment by linearly interpolating
           the wind speed to the height of the segment center in log-height.
        3. Calculate the wind direction at the center of each segment by linearly interpolating
           the wind direction to the height of the segment center. Circularity is
           taken into account here.
        4. Calculate the wind direction at hub height by linearly interpolating the wind
           direction to the hub height.
        5. Calculate the REWS as the cube root of the sum of the wind speed at each segment
           center multiplied by the area-weight (area/total) of the segment and the cosine
           of the difference between the wind direction at the segment center and the wind
           direction at hub height.

    Parameters
    ----------
    wind_speed : xarray.DataArray
        Wind speed on height levels.
    wind_direction : xarray.DataArray
        Wind direction on height levels.
    hub_height : float
        Turbine Hub height.
    rotor_diameter : float
        Turbine rotor diameter.
    delta_z : float, optional
        Height difference between segments of turbine spanned rotor area
        (default: 1.0).
    n_integrate : int, optional
        Number of points to use for integration (default: 1001) of the area
        of each segment.

    Returns
    -------
    rews : xarray.DataArray
        Rotor equivalent wind speed.

    """

    if not isinstance(wind_speed, xr.DataArray):
        raise TypeError("wind_speed must be a xarray.DataArray")

    if not isinstance(wind_direction, xr.DataArray):
        raise TypeError("wind_direction must be a xarray.DataArray")

    if "height" not in wind_speed.dims:
        raise ValueError("wind_speed must have a height dimension")

    if "height" not in wind_direction.dims:
        raise ValueError("wind_direction must have a height dimension")

    hub_height = float(hub_height)
    rotor_diameter = float(rotor_diameter)
    delta_z = float(delta_z)
    n_integrate = int(n_integrate)

    rotor_radius = rotor_diameter / 2.0

    zi = np.linspace(
        hub_height - rotor_radius,
        hub_height + rotor_radius,
        int(np.round(rotor_diameter / delta_z)) + 1,
    )
    zc = (zi[1:] + zi[:-1]) / 2
    zc = xr.DataArray(zc, dims=("height",), coords={"height": zc})

    Ai = np.zeros_like(zc)

    for i in range(len(zi) - 1):
        zs = np.linspace(zi[i], zi[i + 1], n_integrate)
        Ai[i] = trapezoid(2 * np.sqrt(rotor_radius**2 - (zs - hub_height) ** 2), zs)

    # Area of rotor
    A = np.pi * rotor_radius**2

    # Area of rotor segment
    Ai = xr.DataArray(Ai, dims=("height",), coords={"height": zc})

    # wind speed and direction at segment center
    ui = vinterp_wind_speed(
        wind_speed, zc, method="linear", kwargs={"fill_value": "extrapolate"}
    )
    di = vinterp_wind_direction(
        wind_direction, zc, method="linear", kwargs={"fill_value": "extrapolate"}
    )

    # wind direction at hub height
    dh = vinterp_wind_direction(
        wind_direction,
        hub_height,
        method="linear",
        kwargs={"fill_value": "extrapolate"},
    )

    rews = ((1 / A) * Ai * (ui**3) * np.cos(np.deg2rad(di - dh))).sum(dim="height")

    rews = xr.where(rews < 0, 0, rews)

    rews = np.power(rews, 1.0 / 3.0)

    rews = rews.expand_dims(height=[hub_height])

    return rews


def resample_wind_and_direction(
    ds,
    freq,
    var_ws="wind_speed",
    var_wd="wind_direction",
    min_availability=0.5,
    **kwargs,
):
    """Resample wind speed and direction to a given frequency.

    Parameters
    ----------
    ds : xarray.Dataset
        Dataset with wind speed and direction.
    freq : str
        Resampling frequency.
    var_ws : str, optional
        Name of wind speed variable, by default "wind_speed".
    var_wd : str, optional
        Name of wind direction variable, by default "wind_direction".

    Returns
    -------
    xarray.Dataset
        Resampled dataset.

    """
    ds = ds.copy()

    def nan_mean(da):
        return da.mean(dim="time").where(
            da.notnull().sum(dim="time") >= len(da.time) * min_availability
        )

    ds["__U__"], ds["__V__"] = wind_vectors(ds[var_ws], ds[var_wd])
    ds = ds.drop_vars([var_ws, var_wd])
    ds = ds.resample(time=freq, **kwargs).map(nan_mean)

    ds[var_ws], ds[var_wd] = wind_speed_and_direction(ds["__U__"], ds["__V__"])
    ds = ds.drop_vars(["__U__", "__V__"])
    return ds
