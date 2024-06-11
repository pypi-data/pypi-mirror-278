# (c) 2022 DTU Wind Energy
"""
Routines for working with the sector coordinate.
"""
import numpy as np
import xarray as xr

from .metadata import _SECTOR_COORD_ATTRS, _WSBIN_COORD_ATTRS, update_history


def create_ws_bin_coords(bin_width=1.0, nws=40):
    """Create wind speed bins coordinates from a bin width and a number of bins.

    Create a data array with the wind speed bins, ceiling and floor.

    Parameters
    ----------
    bin_width : float
        Wind speed bin width, defaults to 1.0
    nws : int
        Number of wind speed bins, defaults to 40.

    Returns
    -------
    cen_da : xarray.DataArray
        Data array with wind speed bins.
    """

    if type(nws) is not int:
        raise TypeError("'nws' argument must be integer")
    if bin_width <= 0.0:
        raise ValueError("'bin_width' argument must be positive")
    if nws <= 0:
        raise ValueError("'nws' argument must be positive")

    cen_vals = np.linspace(bin_width / 2, float(nws) * bin_width - bin_width / 2, nws)
    # Create data arrays of sector valuse
    cen_da = xr.DataArray(cen_vals, dims="wsbin")
    ceil_da = xr.DataArray(cen_vals + 0.5 * bin_width, dims="wsbin")
    floor_da = xr.DataArray(cen_vals - 0.5 * bin_width, dims="wsbin")

    cen_da = cen_da.assign_coords(
        {
            "wsbin": cen_da,
            "wsceil": ceil_da,
            "wsfloor": floor_da,
        }
    )
    cen_da["wsbin"].attrs = {
        **_WSBIN_COORD_ATTRS["wsbin"],
        "bin_width": str(bin_width),
    }
    cen_da["wsceil"].attrs = {**_WSBIN_COORD_ATTRS["wsceil"]}
    cen_da["wsfloor"].attrs = {**_WSBIN_COORD_ATTRS["wsfloor"]}

    return cen_da


def create_ws_bin_coords_from_values(wsbins):
    """Create wind speed bins coordinates from an array of bins.

    Create a data array with the wind speed bins, ceiling and floor.

    Parameters
    ----------
    wsbins : numpy.ndarray or array_like
        1D array with wind speed bins.
    Returns
    -------
    cen_da : xarray.DataArray
        Data array with wind speed bins.
    """

    try:
        wsbins = np.asfarray(wsbins)
    except:
        raise TypeError(
            "'wsbins' is not a numpy.ndarray or array_like of wind speed bins"
        )

    if wsbins.ndim != 1:
        raise ValueError("'wsbins' has to be a 1D numpy.ndarray or array_like")

    cen_vals = 0.5 * (wsbins[:-1] + wsbins[1:])
    # Create data arrays of sector valuse
    cen_da = xr.DataArray(cen_vals, dims="wsbin")
    ceil_da = xr.DataArray(wsbins[1:], dims="wsbin")
    floor_da = xr.DataArray(wsbins[:-1], dims="wsbin")

    cen_da = cen_da.assign_coords(
        {
            "wsbin": cen_da,
            "wsceil": ceil_da,
            "wsfloor": floor_da,
        }
    )
    cen_da["wsbin"].attrs = {**_WSBIN_COORD_ATTRS["wsbin"]}
    cen_da["wsceil"].attrs = {**_WSBIN_COORD_ATTRS["wsceil"]}
    cen_da["wsfloor"].attrs = {**_WSBIN_COORD_ATTRS["wsfloor"]}

    return cen_da


def create_sector_coords(nsec):
    """Create wind sector coordinate as a data array.

    The data array contains the sector, the sector ceiling and the
    sector floor.

    Parameters
    ----------
    nsec : int
        Number of sectors to create

    Returns
    -------
    cen_da : xarray.DataArray
        Data array with sector coordinates, ceiling and floor.
    """
    if type(nsec) not in [np.int32, np.int64, int]:
        raise TypeError("'nsec' must be of integer type")
    if nsec <= 0:
        raise ValueError("'nsec' must be a positive integer")

    sec_width = 360 / nsec
    cen_vals = np.linspace(0.0, 360.0 - sec_width, nsec)

    # Create data arrays of sector valuse
    cen_da = xr.DataArray(cen_vals, dims="sector")
    ceil_da = xr.DataArray((cen_vals + 0.5 * sec_width) % 360, dims="sector")
    floor_da = xr.DataArray((cen_vals - 0.5 * sec_width) % 360, dims="sector")

    cen_da = cen_da.assign_coords(
        {
            "sector": cen_da,
            "sector_ceil": ceil_da,
            "sector_floor": floor_da,
        }
    )
    cen_da["sector"].attrs = {
        **_SECTOR_COORD_ATTRS["sector"],
        "bin_width": str(sec_width),
    }
    cen_da["sector_ceil"].attrs = {**_SECTOR_COORD_ATTRS["sector_ceil"]}
    cen_da["sector_floor"].attrs = {**_SECTOR_COORD_ATTRS["sector_floor"]}

    return cen_da


def create_sector_coords_from_edges(sectors_array):
    """Create sector coordinates from an array of sector edges.

    Create a data array with the sector centers, ceiling and floor.

    Parameters
    ----------
    wsbins : numpy.ndarray or array_like
        1D array with sector edges.
    Returns
    -------
    cen_da : xarray.DataArray
        Data array with sector edges.
    """
    sectors_da = create_ws_bin_coords_from_values(sectors_array)
    sectors_da = sectors_da.rename(
        {"wsbin": "sector", "wsceil": "sector_ceil", "wsfloor": "sector_floor"}
    )
    # Update coordinate attribures
    sectors_da["sector"].attrs = {
        **_SECTOR_COORD_ATTRS["sector"],
    }
    sectors_da["sector_ceil"].attrs = {**_SECTOR_COORD_ATTRS["sector_ceil"]}
    sectors_da["sector_floor"].attrs = {**_SECTOR_COORD_ATTRS["sector_floor"]}

    return update_history(sectors_da)


def create_direction_coords(nsec=None, direction=None):
    """Create wind direction coordinate as a DataArray

    Wind direction coordinates use "sector" as their dimension, but represent a single
    wind direction rather than a sectoral region.

    Parameters
    ----------
    nsec : int, optional
        Number of sectors to create, by default None. If None, direction must be specified.
    direction : float, optional
        Wind direction to set, by default None. If None, nsec must be specified.

    Returns
    -------
    dir_da : xarray.DataArray
        Data array with direction coordinates.

    """

    if nsec is not None and direction is not None:
        raise ValueError("Must only set one of nsec and direction.")
    if nsec is not None:
        sec_width = 360 / nsec
        direction = np.linspace(0.0, 360.0 - sec_width, nsec)
    else:
        direction = np.array([direction], np.float32)

    # Create data arrays of sector valuse
    dir_da = xr.DataArray(direction, dims="sector")
    dir_da = dir_da.assign_coords({"sector": dir_da})
    dir_da["sector"].attrs = {**_SECTOR_COORD_ATTRS["wind_direction"]}

    return dir_da
