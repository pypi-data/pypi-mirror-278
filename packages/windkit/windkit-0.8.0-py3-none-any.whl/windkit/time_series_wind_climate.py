# (c) 2022 DTU Wind Energy
"""Time series wind climate module

A time series wind climate is defined by dataset with a time series
``wind speed`` and ``wind direction``.

A valid time series wind climate therefore has a dimension ``time``.
Also it must have one of the valid :ref:`geospatial_structures`. This module contains
functions that operate on time series wind climates.
This includes the ability to create time series datasets from files and from
existing data.
"""

import collections
import re
import warnings

import numpy as np
import pandas as pd
import xarray as xr

from ._errors import WindClimateValidationError
from ._validate import create_validator
from .metadata import _TS_ATTRS, update_history, update_var_attrs
from .spatial import to_stacked_point
from .spatial._crs import add_crs

WS = "wind_speed"
WD = "wind_direction"
DIM_TIME = "time"
DATA_VAR_DICT_TS = {WS: [DIM_TIME], WD: [DIM_TIME]}
REQ_DIMS_TS = [DIM_TIME]
REQ_COORDS_TS = ["south_north", "west_east", "height", "crs"]


ts_validate, ts_validate_wrapper = create_validator(
    DATA_VAR_DICT_TS, REQ_DIMS_TS, REQ_COORDS_TS
)


def _is_ts(wco):
    """Check if this is a times series wind climate

    Returns true if tswc and false if not

    Parameters
    ----------
    wco: xarray.Dataset
        Wind Climate Object

    Returns
    -------
    Bool
        Returns true if tswc and false if not
    """
    try:
        ts_validate(wco)
        return True
    except WindClimateValidationError:
        return False


def read_ts_windpro_txt(fpath):
    """Parses windpro format txt file into a dataset.



    Parameters
    ----------
    fpath : [str]
        [file path to be parsed]

    Returns
    -------
    xarray.Dataset

    """

    def _is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    # parse parameters from windpro header;
    lng, lat = 0.0, 0.0
    data_start_line = -1
    disp_height = -1
    with open(fpath, "r") as file:
        for i, line in enumerate(file):
            # parse coordinates
            if "Geographical Coordinates" in line:
                parts = line.split()
                for j, p in enumerate(parts):
                    if _is_float(p) and parts[j - 1] == "Longitude:":
                        lng = float(p)
                    if _is_float(p) and parts[j - 1] == "Latitude:":
                        lat = float(p)
            # parse height
            if "Displacement height" in line:
                parts = line.split()
                for p in parts:
                    if _is_float(p):
                        disp_height = float(p)
            # reached header
            if "TimeStamp" in line:
                data_start_line = i
                break

    if disp_height > 0:
        warnings.warn(
            "Displacement height cannot be used in WindKit. Set it up via the map instead."
        )
    if lng == 0.0 and lat == 0.0:
        raise Exception("Couldn't parse coordinates")

    ts = pd.read_csv(
        fpath,
        delimiter="\t{2}|\t",
        parse_dates=["TimeStamp"],
        skiprows=range(data_start_line),
        engine="python",
    )

    # parse height from the wind speed/direction column
    for col in ts.columns:
        if "Mean wind speed" in col:
            height = float(re.findall(r"[0-9]+.[0-9]+m", col)[0].replace("m", ""))
            ts = ts.rename({col: "ws"}, axis="columns")
        if "Wind direction" in col:
            ts = ts.rename({col: "wd"}, axis="columns")

    ts = ts[~ts.ws.str.contains("-")]
    ts = ts[ts["ws"].notna()]
    ts = ts[ts["wd"].notna()]
    ts["ws"] = ts["ws"].astype(float)
    ts["wd"] = ts["wd"].astype(float)

    ts_ds = xr.Dataset(
        {
            "wind_speed": (["time"], ts["ws"]),
            "wind_direction": (["time"], ts["wd"]),
        },
        coords={
            "time": ("time", ts["TimeStamp"]),
            "south_north": lat,
            "west_east": lng,
            "height": height,
            "crs": 0,
        },
    )

    add_crs(ts_ds, 4326)
    update_var_attrs(ts_ds, {**_TS_ATTRS})
    # validate the dataset before returning
    ts_validate(ts_ds)
    return ts_ds


def read_timeseries_from_csv(
    csv_filename,
    west_east,
    south_north,
    crs,
    time_col=0,
    height_to_columns=None,
    **kwargs,
):
    """
    Reads a csv file into a time series wind climate xarray.Dataset. The file must have one time
    entry per row, a column with a time stamp and at least one wind speed and one wind direction. It
    allows to create a dataset for several heights.

    Parameters
    ----------
    csv_filename : str
        file path to a csv file with wind speed and wind direction measurements for different timestamps.
    west_east: float
        west east locaton of the measurement
    south_north: float
        south north location of the measurement
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
    time_col: int, str
        column position (integer) or header (str) where the timestamp is located. it can be overriden by
        using `pandas.read_csv` kwargs. Defaults to 0 (first column in the file).
    height_to_columns: dict
        dictionary to map the wind speed and directions to its corresponding height. The key is a float
        with the height, and the value is a tuple (str,str) with the header for the wind speed and the
        header for the wind direction, respectively. If the parameter is `None`, the columns are inferred
        from the column names in the files. The function will find wind speeds for different heights and
        after that will look for wind direction columns, matching them to the closest height.
        Examples of autodetected header formats:

            - ws_10, ws_10_mean, ws10, WS10 (wind speed at 10 m)
            - windagl10, windagl_10, windagl_10_mean (wind speed at 10 m)
            - wd_15, wd_15_mean, w15, WD15 (wind direction at 15m)
            - wdiragl15, wdiragl_15, wdiragl_15_mean (wind direction at 15 m)

    ``**kwargs``: dict
        Optional arguments that are forwarded to `pandas.read_csv` for customizing its behavior.

    Returns
    -------
    da: xarray.Dataset
        Time series wind climate dataset  with variables 'wind_speed' and 'wind_direction'
        and with a coordinate and dimension 'time'.
    Raises
    ------
    RuntimeError
        If the time column cannot be parsed or if the wind speed and wind direction columns cannot
        be detected.
    """

    default_kwargs = {
        "parse_dates": True,
        "index_col": time_col,
    }

    kwargs = {**default_kwargs, **kwargs}

    pd_df = pd.read_csv(csv_filename, **kwargs)

    return read_timeseries_from_pandas(
        pd_df, west_east, south_north, crs, height_to_columns
    )


def read_timeseries_from_pandas(
    pd_df,
    west_east,
    south_north,
    crs,
    height_to_columns=None,
):
    """
    transforms a pandas.DataFrame into a time series wind climate xarray.Dataset. The dataframe must have
    an index with time format and at least one wind speed and one wind direction. It allows to create a
    dataset for several heights.

    Parameters
    ----------
    pd_df : pandas.DataFrame
        pandas dataframe with wind speed and wind direction measurements for different timestamps and
        heights.
    west_east: float
        west east locaton of the measurement
    south_north: float
        south north location of the measurement
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
    height_to_columns: dict
        dictionary to map the wind speed and directions to its corresponding height. The key is a float
        with the height, and the value is a tuple (str,str) with the header for the wind speed and the
        header for the wind direction, respectively. If the parameter is `None`, the columns are inferred
        from the column names in the dataframe. The function will find wind speeds for different heights
        and after that will look for wind direction columns, matching them to the closest height.
        Examples of autodetected header formats:

           - ws_10, ws_10_mean, ws10, WS10 (wind speed at 10 m)

           - windagl10, windagl_10, windagl_10_mean (wind speed at 10 m)

           - wd_15, wd_15_mean, w15, WD15 (wind direction at 15m)

           - wdiragl15, wdiragl_15, wdiragl_15_mean (wind direction at 15 m)

    Returns
    -------
    da: xarray.Dataset
        Time series wind climate dataset with variables 'wind_speed' and 'wind_direction'
        and with a coordinate and dimension 'time'.
    Raises
    ------
    RuntimeError
        If it fails to autodetect the columns
    """
    # Check if index is datetime
    if not isinstance(pd_df.index, pd.DatetimeIndex):
        raise RuntimeError(
            "The dataframe index is not of type 'datetime'. Please provide a pandas.DataFrame with the time as index."
        )

    if height_to_columns is None:
        try:
            height_to_columns = _headers_to_dict(pd_df)
            print("Columns detected")
            print("{:<5} {:<12} {:<12}".format("h", "Wind speed", "Wind dir"))
            for k, v in height_to_columns.items():
                print("{:<5} {:<12} {:<12}".format(k, v[0], v[1]))

        except Exception as err:
            raise RuntimeError(
                str(err)
                + "\nColumns could not be detected automatically. Provide a height_to_columns dictionary."
            )

    ds_pieces = []
    for k, v in height_to_columns.items():
        ws = xr.DataArray(pd_df[v[0]], dims=["time"])
        wd = xr.DataArray(pd_df[v[1]], dims=["time"])
        ds_piece = xr.Dataset({"wind_speed": ws, "wind_direction": wd}).assign_coords(
            height=k,
        )
        ds_pieces.append(ds_piece)

    ds = xr.concat(ds_pieces, dim="height")
    ds = ds.assign_coords(
        {
            "west_east": west_east,
            "south_north": south_north,
        }
    )
    ds = ds.transpose("time", ...)
    ds = add_crs(ds, crs)
    ds = update_history(ds)
    return to_stacked_point(update_var_attrs(ds, {**_TS_ATTRS}))


def _headers_to_dict(df):
    """
    Tries to detect the wind speed and wind direction columns on a pandas dataframe
    and builds a dictionary

    Parameters
    ----------
    df : pandas.DataFrame
        dataframe with wind data

    Returns
    -------
    dict: Dictionary where the key is the height (float) and the value is a tuple (string,string)
    with the wind speed column header and the wind direction column header, or None if the headers
    format does not allow autodetection.
    """
    headers_list = df.columns
    vel_columns, dir_columns = _parse_heights_from_headers(headers_list)
    if len(vel_columns) == 0:
        raise RuntimeError("No wind speed columns were found.")
    if len(dir_columns) == 0:
        raise RuntimeError("No wind direction columns were found.")
    v_list = np.array([x[0] for x in vel_columns])
    d_list = np.array([x[0] for x in dir_columns])
    duplicate_heights = [
        x for x, count in collections.Counter(v_list).items() if count > 1
    ]
    if len(duplicate_heights) > 0:
        duplicate_heights_err_msg = ""
        for val in duplicate_heights:
            duplicate_heights_err_msg += (
                f"There are duplicate entries for height {val}\n"
            )
        raise RuntimeError(duplicate_heights_err_msg.rstrip())

    indices = _closest_dir_index(v_list, d_list)

    final_dict = {}
    for i, val in enumerate(vel_columns):
        final_dict.update({val[0]: (val[1], dir_columns[indices[i]][1])})

    return final_dict


def _parse_heights_from_headers(header_list):
    """Detect the wind speed and wind direction columns from a header list

    Parameters
    ----------
    header_list : list of string
        list with each header

    Returns
    -------
    list: list with tuples (float,string) with the height and the string header of the wind speed
    list: list with tuples (float,string) with the height and the string header of the wind direction
    """
    response_h = []
    response_d = []
    velocity_patterns_list = [
        r"(?:(?:windagl)|(?:ws))_*(?P<height>\d*\.*\d+).*(?:mean)*",
        r"a(?P<height>\d*\.*\d+)(:?(:?|:?T0deg))_wind_speed_mean",
    ]
    direction_patterns_list = [
        r"(?:(?:wdiragl)|(?:wd))_*(?P<height>\d*\.*\d+).*(?:mean)*",
        r"d(?P<height>\d*\.*\d+)(:?(:?|:?T0deg))_wind_direction_mean",
    ]

    while len(velocity_patterns_list) != 0:
        velocity_pattern = velocity_patterns_list.pop(0)
        direction_pattern = direction_patterns_list.pop(0)
        for val in header_list:
            match_vel = re.match(velocity_pattern, val, re.IGNORECASE)
            match_dir = re.match(direction_pattern, val, re.IGNORECASE)
            if match_vel is not None:
                height_vel = match_vel.group("height")
                response_h.append((float(height_vel), val))
            if match_dir is not None:
                height_dir = match_dir.group("height")
                response_d.append((float(height_dir), val))

    return response_h, response_d


def _closest_dir_index(vel_list, dir_list):
    """
    returns  a list with the indices with the closest value of wind
    direction for a given wind velocity

    Parameters
    ----------
    vel_list : numpy.array
        array with heights where the velocity was measured
    dir_list : numpy.array
        array with height where the direction was measured

    Returns
    -------
    list : list
        list with the indices in dir_list corresponding to vel_list
    """
    resp = []
    for val in vel_list:
        resp.append(np.argmin(abs(val - dir_list)))
    return resp
