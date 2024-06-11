# (c) 2022 DTU Wind Energy
"""Weibull wind climate module

When measuring over a long period the frequency of occurence of wind speed usually follows a
`Weibull distribution <https://en.wikipedia.org/wiki/Weibull_distribution>`_. It is therefore common
practice in the wind energy industry to use the Weibull *A* and *k*
parameters to denote the wind resource at a certain location.

Because there can be large differences in the wind climate when the wind is
coming from different wind directions, the Weibull distributions are usually specified
per sector.

A valid Weibull wind climate therefore has a dimension ``sector`` and the variables
``A``, ``k`` and ``wdfreq``. Also it must have a valid spatial structure. This module contains
functions that operate on and create weibull wind climates.
"""
import io
import logging
import re
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
from scipy.special import gamma

from ._errors import WindClimateValidationError
from ._validate import create_validator
from .metadata import _BWC_ATTRS, _WEIB_ATTRS, update_history, update_var_attrs
from .sector import create_sector_coords, create_ws_bin_coords_from_values
from .spatial import (
    _raster,
    add_crs,
    count_spatial_points,
    crs_are_equal,
    is_cuboid,
    to_raster,
)
from .weibull import fit_weibull_k_sumlogm, weibull_cdf, weibull_moment

WRG_HEADER_PATTERN = re.compile(
    r"\s*(\d+)\s+(\d+)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s*",
    re.IGNORECASE,
)

DATA_VAR_DICT_WWC = {"A": ["sector"], "k": ["sector"], "wdfreq": ["sector"]}

REQ_DIMS_WWC = ["sector"]

REQ_COORDS_WWC = [
    "south_north",
    "west_east",
    "height",
    "crs",
    "sector",
    "sector_ceil",
    "sector_floor",
]


def _validate_values_range(wwc):
    """Helper function to validate data variables are within range"""
    response_list = []

    if "A" in wwc.data_vars and any(
        xr.where(wwc.A.sum(dim="sector") <= 0.0, True, False).values.flatten()
    ):
        response_list.append("Sum of A values not positive.")

    if "k" in wwc.data_vars and any(
        xr.where(wwc.k == 0.0, True, False).values.flatten()
    ):
        response_list.append("At least one of the k values is zero.")

    if "wdfreq" in wwc.data_vars and "sector" in wwc.wdfreq.dims:
        sum_s = wwc["wdfreq"].sum(dim="sector")
        if not np.allclose(sum_s, 1.0):
            response_list.append("Wind direction frequency must sum to 1")

    return response_list


wwc_validate, wwc_validate_wrapper = create_validator(
    DATA_VAR_DICT_WWC,
    REQ_DIMS_WWC,
    REQ_COORDS_WWC,
    checks_iterator=[_validate_values_range],
)

wwc_validate_structure, wwc_validate_structure_wrapper = create_validator(
    DATA_VAR_DICT_WWC,
    REQ_DIMS_WWC,
    REQ_COORDS_WWC,
    checks_iterator=[],
)


def _is_wwc(wco):
    """Check if a wind climate is a bwc?

    Returns true if bwc and false if not

    Parameters
    ----------
    wco: xarray.Dataset
        Wind Climate

    Returns
    -------
    Bool
        Returns true if bwc and false if not
    """
    try:
        wwc_validate_structure(wco)
        return True
    except WindClimateValidationError:
        return False


def _get_A_k(wwc, bysector):  # pylint:disable=invalid-name
    """Return the appropriate A & k values from the wwc

    Parameters
    ----------
    wwc: xarray.Dataset
        Weibull Wind Climate object
    bysector: bool
        Should results be returned by sector?

    Returns
    -------
    tuple of xr.DataArray
        A & k DataArrays extracted from wwc
    """
    if bysector:
        A = wwc["A"]
        k = wwc["k"]
    elif "A_combined" in wwc.variables:
        A = wwc["A_combined"]
        k = wwc["k_combined"]
    else:
        A, k = weibull_combined(wwc)

    return A, k


def _has_wrg_header(infile, parse_header=False):
    """Check if a resource file has a WRG-style header
    and optionally parse the params.

    Parameters
    ----------
    infile : str, pathlib.Path, io.StringIO
        Input file to check
    parse_header : bool, optional
        If True, will attemp to parse the header params, by default False

    Returns
    -------
    bool:
        Whether the file has a wrg header
    GridParams, optional:
        Grid parameters parsed from the header, if parse_header=True

    """
    if isinstance(infile, io.StringIO):
        fobj = infile
    else:
        fobj = open(infile)

    line = fobj.readline().strip()

    if not isinstance(infile, io.StringIO):
        fobj.close()

    match = WRG_HEADER_PATTERN.match(line)

    return bool(match)


def _infer_resource_file_nsec(infile, skip_first=True):
    """Infer the number of sectors in resource file by reading
    column 70-72 and converting it to an integer.

    Parameters
    ----------
    infile : str, pathlib.Path, io.StringIO
        Resource file to infer sectors from.

    Returns
    -------
    int
        Number of sectors
    """
    if isinstance(infile, io.StringIO):
        fobj = infile
    else:
        fobj = open(infile)

    # Skip the first line
    if skip_first:
        fobj.readline()

    # Read the second line
    line = fobj.readline()

    if not isinstance(infile, io.StringIO):
        fobj.close()

    return int(line[69:72])  # column 70-72 using python indexing


def _read_resource_file(
    resource_file, crs, nsec=12, to_cuboid=False, use_production=False, **kwargs
):
    """Reads .wrg or .rsf file into a weibull wind climate dataset.

    Parameters
    ----------
    resource_file : str, pathlib.Path, io.StringIO
        Path to resource file
    crs : int, dict, str or CRS
        Value to create CRS object or an existing CRS object
    nsec : int
        Number of sectors in file. Defaults to 12.
    to_cuboid: boolean
        If true, the dataset will be converted to the cuboid spatial
        structure (dimensions south_north, west_east, height).
    use_production: bool
        If True, the column with power in the file is interpreted as power production,
        i.e. stored as 'gross_aep' in the dataset. If False, it is stored as 'power_density'.
        If the values in the file are power production, they are originally storedin Wh/y,
        but they are saved with units GWh/y in the dataset.  Defaults to False.

    Returns
    -------
    wwc: xarray.Dataset
        Weibull wind climate dataset.
    """
    if crs is None:
        raise ValueError("crs must be specified")

    has_wrg_header = _has_wrg_header(resource_file)
    nsec = _infer_resource_file_nsec(resource_file, skip_first=has_wrg_header)

    df = pd.read_fwf(
        resource_file,
        widths=tuple([10, 10, 10, 8, 5, 5, 6, 15, 3] + [4, 4, 5] * nsec),
        header=None,
        skiprows=int(has_wrg_header),
    )
    power_col = "gross_aep" if use_production else "power_density"
    header = [
        "name",
        "west_east",
        "south_north",
        "site_elev",
        "height",
        "A_combined",
        "k_combined",
        power_col,
        "nsec",
    ]

    for i in range(1, nsec + 1):
        header += f"f_{i} A_{i} k_{i}".split()

    df.columns = header

    can_be_raster = _raster._can_be_raster(df["west_east"], df["south_north"])

    df = df.set_index(["name"])

    wwc = df.to_xarray()

    wwc = wwc.assign_coords(point=(("name",), np.arange(len(df.index))))
    wwc = wwc.swap_dims({"name": "point"})
    wwc = wwc.drop_vars("point")
    wwc = wwc.assign_coords(
        west_east=(("point",), wwc.west_east.values),
        south_north=(("point",), wwc.south_north.values),
        height=(("point",), wwc.height.values),
    )

    knames = [f"k_{sec}" for sec in range(1, nsec + 1)]
    Anames = [f"A_{sec}" for sec in range(1, nsec + 1)]
    fnames = [f"f_{sec}" for sec in range(1, nsec + 1)]

    wwc["k"] = xr.concat([wwc[n] for n in knames], dim="sector")
    wwc["A"] = xr.concat([wwc[n] for n in Anames], dim="sector")
    wwc["wdfreq"] = xr.concat([wwc[n] for n in fnames], dim="sector")

    wwc["site_elev"] = wwc["site_elev"].astype(np.float64)
    wwc["k"] = wwc["k"] / 100.0
    wwc["A"] = wwc["A"] / 10.0
    wwc["wdfreq"] = wwc["wdfreq"] / wwc["wdfreq"].sum(dim="sector", skipna=False)

    wwc = wwc.drop_vars(
        ["nsec"]
        + [f"f_{sec}" for sec in range(1, nsec + 1)]
        + [f"A_{sec}" for sec in range(1, nsec + 1)]
        + [f"k_{sec}" for sec in range(1, nsec + 1)]
    )

    if use_production:
        wwc["gross_aep"] = wwc["gross_aep"] / 1e9  # Wh/y -> GWh/y
    wwc = add_crs(wwc, crs)
    wdcenters = create_sector_coords(nsec)
    wwc = wwc.assign_coords(**wdcenters.coords)

    n_spatial = count_spatial_points(wwc)

    if (not can_be_raster) and to_cuboid and (n_spatial > 1):
        logging.warning(
            "_read_resource_file: Data cannot be converted to raster, returning point."
        )
    if can_be_raster and to_cuboid or n_spatial == 1 and to_cuboid:
        wwc = to_raster(wwc, ignore_raster_check=True)
        if "elevation" in wwc.data_vars:
            wwc["elevation"] = wwc["elevation"].isel(height=0)

    wwc = update_var_attrs(wwc, _WEIB_ATTRS)
    return update_history(wwc)


def read_rsffile(rsffile, crs, to_cuboid=False, use_production=False, **kwargs):
    """Reads .rsf file into a weibull wind climate dataset.

    Parameters
    ----------
    rsffile : str, pathlib.Path, io.StringIO
        Path to .rsf file
    crs : int, dict, str or CRS
        Value to create CRS object or an existing CRS object
    to_cuboid: boolean
        If true, the dataset will be converted to the cuboid spatial
        structure (dimensions south_north, west_east, height).
    use_production: bool
        If True, the column with power in the file is interpreted as power production,
        i.e. stored as 'gross_aep' in the dataset. If False, it is stored as 'power_density'.
        If the values in the file are power production, they are originally storedin Wh/y,
        but they are saved with units GWh/y in the dataset.  Defaults to False.

    Returns
    -------
    wwc: xarray.Dataset
        Weibull wind climate dataset.
    """
    return _read_resource_file(
        rsffile, crs=crs, to_cuboid=to_cuboid, use_production=use_production, **kwargs
    )


def read_wrgfile(wrgfile, crs=None, to_cuboid=True, use_production=False, **kwargs):
    """Reads .wrg file into a weibull wind climate dataset.

    Parameters
    ----------
    wrgfile : str, pathlib.Path, io.StringIO
        Path to .wrg file
    crs : int, dict, str or CRS
        Value to create CRS object or an existing CRS object
    to_cuboid: boolean
        If true, the dataset will be converted to the cuboid spatial
        structure (dimensions south_north, west_east, height).
    use_production: bool
        If True, the column with power in the file is interpreted as power production,
        i.e. stored as 'gross_aep' in the dataset. If False, it is stored as 'power_density'.
        If the values in the file are power production, they are originally storedin Wh/y,
        but they are saved with units GWh/y in the dataset.  Defaults to False.

    Returns
    -------
    wwc: xarray.Dataset
        Weibull wind climate dataset.
    """
    return _read_resource_file(
        wrgfile, crs=crs, to_cuboid=to_cuboid, use_production=use_production, **kwargs
    )


def read_pwcfile(pwcfile, spatial_dataset):
    """Reads .pwc predicted wind climate file from WAsP in XML format.
       The .pwc file does not include spatial information, so it must
       be passed as a parameter.

    Parameters
    ----------
    pwcfile: str,pathlib.Path, io.StringIO
        Path to .pwc file
    spatial_dataset: xarray.Dataset
        xarray dataset with the spatial info
    """
    ds = pd.read_xml(
        pwcfile, names=["index", "sector", "sector_width", "wdfreq", "A", "k"]
    )
    ds = ds.set_index("sector")[["A", "k", "wdfreq"]].to_xarray()
    ds = ds.assign_coords(create_sector_coords(ds.sector.size).coords)
    ds = ds.expand_dims(spatial_dataset.dims)
    ds = ds.assign_coords(spatial_dataset.coords)
    wwc = update_var_attrs(ds, _WEIB_ATTRS)
    return update_history(wwc)


def _can_be_int(x):
    """Check if x can be converted to int."""
    try:
        int(x)
        return True
    except ValueError:
        return False


def _convert_to_int_or_fixed_decimals(x, decimals=1):
    if _can_be_int(x):
        return int(x)
    else:
        return np.round(x, decimals=decimals)


def _wrg_header(wwc):
    """Write WWC grid dimensions to WRG header with the format:
          nx ny xmin ymin cell_size

    Parameters
    ----------
    wwc : xarray.Dataset
        Weibull wind climate xarray dataset.

    Returns
    -------
    str
        WRG header.

    """
    nx, ny = _raster._shape(wwc)
    xmin = _convert_to_int_or_fixed_decimals(wwc.west_east.values.min(), decimals=1)
    ymin = _convert_to_int_or_fixed_decimals(wwc.south_north.values.min(), decimals=1)
    size = _convert_to_int_or_fixed_decimals(_raster._spacing(wwc), decimals=1)
    return f" {nx:<13} {ny:<13} {xmin:>9} {ymin:>13} {size:>8}"


def _get_rsf_formatters(df, nsec=12, use_production=False, formatters=None):
    """Returns a list of functions to format the data in the RSF/WRG file.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe with the data to be formatted.

    var_power : str
        Name of the variable to be used as power/aep.

    nsec : int
        Number of sectors.

    use_production : bool
        If true, the gross_aep variable will be used instead of power_density.

    formatters : dict
        Dictionary with the variable names as keys and the functions to format
        the data as values.

    Returns
    -------
    list
        List of functions to format the data in the RSF/WRG file.
    """

    var_power = "gross_aep" if use_production else "power_density"

    fixed_columns = [
        "name",
        "west_east",
        "south_north",
        "elevation",
        "height",
        "A_combined",
        "k_combined",
        var_power,
        "nsec",
    ]

    _formatters_default = {
        "name": lambda x: f"{x:<10}",  # 10
        "west_east": lambda x: f"{x:>9.1f}",  # 10
        "south_north": lambda x: f"{x:>9.1f}",  # 10
        "elevation": lambda x: f"{x:>7.0f}",  # 8
        "height": lambda x: f"{x:>4.1f}",  # 5
        "A_combined": lambda x: f"{x:>4.2f}",  # 5
        "k_combined": lambda x: f"{x:>5.3f}",  # 6
        "power_density": lambda x: f"{x:>14.4f}",  # 15
        "gross_aep": lambda x: f"{x:>14.0f}",  # 15
        "nsec": lambda x: f"{x:>2}",  # 3
        "A": lambda x: f"{x:>3.0f}",  # 4
        "k": lambda x: f"{x:>4.0f}",  # 4
        "wdfreq": lambda x: f"{x:>3.0f}",  # 5
    }
    if formatters is None:
        formatters = _formatters_default
    else:
        formatters = {**_formatters_default, **formatters}

    #
    #  INDIVIDUAL CHECKS AND FORMATTER ADJUSTMENTS
    #

    def _check_max(df, var, maxval):
        vmax = np.abs(df[var]).max()
        if vmax > maxval:
            raise ValueError(
                f"The {var} of one or more points is larger than {maxval}. "
                f"Please check the {var}."
            )

    # name: 10(10)
    if df["name"].str.len().max() > 10:
        raise ValueError(
            "The name of one or more points is longer than 10 characters. "
            "Please shorten the names."
        )

    # west_east: 10(9)
    _check_max(df, "west_east", 99999999)

    if np.abs(df["west_east"]).max() > 999999:
        formatters["west_east"] = lambda x: f"{x:>9.0f}"

    # south_north: 10(9)
    _check_max(df, "south_north", 99999999)

    if np.abs(df["south_north"]).max() > 999999:
        formatters["south_north"] = lambda x: f"{x:>9.0f}"

    # elevation: 8(7)
    _check_max(df, "site_elev", 999999)

    if np.abs(df["site_elev"]).max() > 9999:
        formatters["elevation"] = lambda x: f"{x:>7.0f}"

    # height: 5(4)
    _check_max(df, "height", 9999)

    # When heights are > 100m, the height needs to be written as an integer
    if df["height"].max() > 100.0:
        formatters["height"] = lambda x: f"{x:>4.0f}"

    # A_combined: 5(4)
    _check_max(df, "A_combined", 9999)

    if df["A_combined"].max() >= 10.0:
        formatters["A_combined"] = lambda x: f"{x:>4.1f}"
    elif df["A_combined"].max() >= 100.0:
        formatters["A_combined"] = lambda x: f"{x:>4.0f}"

    # k_combined: 6(5)
    _check_max(df, "k_combined", 99999)

    if df["k_combined"].max() >= 10.0:
        formatters["k_combined"] = lambda x: f"{x:>5.2f}"
    elif df["k_combined"].max() >= 100.0:
        formatters["k_combined"] = lambda x: f"{x:>5.1f}"
    elif df["k_combined"].max() >= 1000.0:
        formatters["k_combined"] = lambda x: f"{x:>5.0f}"

    # power_density / gross_aep: 15(14)
    _check_max(df, var_power, 99999999999999)

    # When all values are missing for power/aep, i.e. valued as -9999,
    # the value needs to be written as an integer
    if all(df[var_power] == -9999):
        formatters[var_power] = lambda x: f"{x:>14.0f}"

    if df[var_power].max() >= 10000000000:
        formatters[var_power] = lambda x: f"{x:>14.1f}"
    elif df[var_power].max() >= 100000000000:
        formatters[var_power] = lambda x: f"{x:>14.0f}"

    # nsec: 3(2)
    _check_max(df, "nsec", 99)

    for isec in range(nsec):
        # A: 4(3)
        _check_max(df, str(("A", isec)), 999)

        # k: 4(3)
        _check_max(df, str(("k", isec)), 999)

        # wdfreq: 5(3)
        _check_max(df, str(("wdfreq", isec)), 9999)

    formatters_list = []
    for col in fixed_columns:
        formatters_list.append(formatters[col])

    for isec in range(nsec):
        formatters_list.append(formatters["wdfreq"])
        formatters_list.append(formatters["A"])
        formatters_list.append(formatters["k"])

    return formatters_list


def _to_resource_file(
    wwc,
    /,
    rsffile,
    wrg_header=False,
    use_production=False,
    formatters=None,
    **kwargs,
):
    """Write weibull wind climate dataset to a resource file (.rsf or .wrg).

    Parameters
    ----------
    wwc : xarray.Dataset
        Weibull wind climate xarray dataset.

    rsffile : str
        Path to resource file

    wrg_header : bool
        If True, the WRG header will be added to the file.
        Requires a cuboid dataset.

    use_production : bool
        If true, the "gross_aep" variable will be used instead of "power_density".

    formatters : dict
        Dictionary with the variable names as keys and the functions to format
        the data as values.

        For each variable the expected widths in the formatter are:
            name: 10
            west_east: 9
            south_north: 9
            elevation: 7
            height: 4
            A_combined: 4
            k_combined: 5
            power_density: 14
            gross_aep: 14
            nsec: 2
            A: 3
            k: 4
            wdfreq: 3

        A space is added after each variable. Meaning the effective
        width of the string representation of the variable is the
        width in the formatter plus one (except for the first variable)

        A formatter can look like:
            formatters  = {
                "west_east": lambda x: f"{x:<9.2f}",
            }

        In this case the width of the string representation of the
        west_east variable will be 10 (9+1). And the number of decimals
        will be 2 instead of the default 1. If a int representation
        is desired, "{x:<9.0f}" can be used.

    """

    # Check if wwc has unsupported dimensions
    approved_dims = [
        "sector",
        "point",
        "stacked_point",
        "south_north",
        "west_east",
        "height",
    ]
    if any([dim not in approved_dims for dim in wwc.dims]):
        raise ValueError(
            f"Unsupported dimensions in wwc: {wwc.dims}. "
            f"Supported dimensions: {approved_dims}"
        )

    if use_production and "gross_aep" not in wwc.data_vars:
        raise ValueError(
            "The gross_aep variable is required to write a resource file with "
            "use_production=True."
        )

    if use_production:
        var_power = "gross_aep"
    else:
        var_power = "power_density"

    wwc_cp = wwc.copy()

    if wrg_header:
        if not is_cuboid(wwc):
            raise ValueError("WWC must be a 'cuboid' to add WRG header!")
        header = _wrg_header(wwc)

    # I feel like it would be cleaner to throw a key error or we always
    # return the parameters required from `downscale()`. But adding the vars
    # as needed works as well.
    if "A_combined" not in wwc_cp.data_vars:
        wwc_cp[["A_combined", "k_combined"]] = weibull_combined(wwc_cp)
    if "wspd" not in wwc_cp.data_vars:
        wwc_cp["wspd"] = wwc_mean_windspeed(wwc_cp)
    if "power_density" not in wwc_cp.data_vars:
        try:
            air_dens = wwc_cp["air_density"]
        except KeyError:
            air_dens = 1.225
        wwc_cp["power_density"] = wwc_power_density(wwc_cp, air_dens)

    # remove unneeded vars
    wwc_cp = wwc_cp.drop_vars(
        ["sector", "sector_ceil", "sector_floor", "crs"], errors="ignore"
    )

    nsec = wwc_cp.sizes["sector"]

    # round values in the order that fits best with WAsP values
    wwc_cp["A"] = wwc_cp["A"].round(decimals=1) * 10.0
    wwc_cp["k"] = wwc_cp["k"].round(decimals=2) * 100.0
    wwc_cp["wdfreq"] = wwc_cp["wdfreq"].round(decimals=3) * 1000.0

    wwc_cp["site_elev"] = wwc_cp["site_elev"].astype(np.int16)
    wwc_cp["nsec"] = xr.full_like(wwc_cp["site_elev"], nsec, dtype=np.int16)

    if use_production:
        wwc_cp["gross_aep"] = wwc_cp["gross_aep"] * 1e9  # GWh/y -> Wh/y

    # select variables that do not depend on wind direction sector
    vars = [
        "name",
        "west_east",
        "south_north",
        "site_elev",
        "height",
        "A_combined",
        "k_combined",
        var_power,
        "nsec",
    ]

    df = wwc_cp[
        ["site_elev", "A_combined", "k_combined", var_power, "nsec"]
    ].to_dataframe()

    if "name" not in df.columns:
        df["name"] = "GridPoint"  # insert text column at first position

    # select variables that depend on wind direction sector
    sec_vars = [str((var, sec)) for sec in range(nsec) for var in ["wdfreq", "A", "k"]]
    df_sec = wwc_cp[["wdfreq", "A", "k"]].to_dataframe()
    df_sec = df_sec.pivot_table(
        index=df.index.names, columns="sector", values=["wdfreq", "A", "k"]
    )

    # merge all-sector and sectorwise values
    df_total = (
        pd.concat([df, df_sec], axis=1)
        .reset_index()
        .drop(["point", "stacked_point"], axis=1, errors="ignore")
    )  # concat combined and sectorwise values
    # transform all column names to string to make it compatible with pandas 1.4
    df_total.columns = [str(x) for x in df_total.columns]
    df_total = df_total[vars + sec_vars]  # select vars in correct order

    formatters_list = _get_rsf_formatters(
        df_total, nsec=nsec, use_production=use_production, formatters=formatters
    )

    str_list = df_total.to_string(
        header=False,
        index=False,
        index_names=False,
        formatters=formatters_list,
    )

    def _is_char_21_blank(s):
        """Check that character 21 is blank."""
        if s[20] != " ":
            return False
        else:
            return True

    def _remove_initial_blank_space(s):
        """Remove initial blank space from each line of the string to be written.
        This is required for the .rsf/.wrg format to get the correct widths written to file.
        """
        sout = ""
        for line in s.split("\n"):
            if line[0] == " ":
                sout += line[1:] + "\n"
        return sout

    def _check_row_widths(s, nsec=12):
        """Check that the row widths are correct for the number of sectors."""
        width_expected = 72 + nsec * 13
        for line in s.split("\n")[:-1]:
            width = len(line)
            if width != width_expected:
                raise ValueError(
                    f".rsf/.wrg row width is {width} Expected {width_expected} for {nsec} sectors!\nare the formatters correct?"
                )

    def _check_ncols(s, nsec=12):
        """Check that the number of columns is correct read back in for the number of sectors."""
        ncols_expected = 9 + nsec * 3
        df = pd.read_fwf(
            io.StringIO(s),
            widths=tuple([10, 10, 10, 8, 5, 5, 6, 15, 3] + [4, 4, 5] * nsec),
            header=None,
        )
        ncols = df.shape[1]
        if ncols != ncols_expected:
            raise ValueError(
                f".rsf/.wrg has {ncols} columns. Expected {ncols_expected} for {nsec} sectors!"
            )

    # check that character 21 is blank and remove initial blank space if not
    # This problem is related to the pandas version (or a dependency of pandas)
    if not _is_char_21_blank(str_list):
        str_list = _remove_initial_blank_space(str_list)

    _check_row_widths(str_list, nsec=nsec)
    _check_ncols(str_list, nsec=nsec)

    with open(rsffile, "w", newline="\r\n") as text_file:
        if wrg_header:
            text_file.write(header + "\n")
        text_file.write(str_list)


@wwc_validate_wrapper
def to_rsffile(
    wwc, rsffile, wrg_header=False, use_production=False, formatters=None, **kwargs
):
    """Write weibull wind climate dataset to .rsf file.

    Parameters
    ----------
    wwc : xarray.Dataset
        Weibull wind climate xarray dataset.
    rsffile: str
        Path to .rsf file
    """
    return _to_resource_file(
        wwc,
        rsffile,
        wrg_header=wrg_header,
        use_production=False,
        formatters=formatters,
        **kwargs,
    )


@wwc_validate_wrapper
def to_wrgfile(wwc, wrgfile, use_production=False, formatters=None):
    """Write weibull wind climate dataset to .wrg file.

    Parameters
    ----------
    wwc : xarray.Dataset
        Weibull wind climate xarray dataset.
    wrgfile: str
        Path to .wrg file
    """
    return _to_resource_file(
        wwc, wrgfile, wrg_header=True, use_production=False, formatters=formatters
    )


def read_grdfile(grdfiles, regex_pattern=None, regex_var_order=None):
    """Reads a .grd file into a weibull wind climate dataset.

    Parameters
    ----------
    grdfiles: str or list
        path of .grd file or list of .grd files.

    regex_pattern: re str
        Filename regex pattern to extract height, sector, and variable name.
        Defaults to None.

    regex_var_order: list or tuple
        Order of 'height', 'sector', and 'var' in regex_pattern. Defaults to None.

    Returns
    -------
    wwc: xarray.Dataset
        Weibull wind climate dataset.
    """

    def _rename_var(var):
        """
        Function to rename WAsP variable names to short hand name
        """
        _rename = {
            "Flow inclination": "flow_inclination",
            "Mean speed": "wspd",
            "Meso roughness": "z0meso",
            "Obstacles speed": "obstacle_speedups",
            "Orographic speed": "orographic_speedups",
            "Orographic turn": "orographic_turnings",
            "Power density": "power_density",
            "RIX": "rix",
            "Roughness changes": "nrch",
            "Roughness speed": "roughness_speedups",
            "Sector frequency": "wdfreq",
            "Turbulence intensity": "turbulence_intensity",
            "Weibull-A": "A",
            "Weibull-k": "k",
            "Elevation": "site_elev",
        }

        return _rename[var]

    def _read_grd_data(filename):
        def _parse_line_floats(f):
            return [float(i) for i in f.readline().strip().split()]

        def _parse_line_ints(f):
            return [int(i) for i in f.readline().strip().split()]

        with open(filename, "rb") as f:
            _ = f.readline().strip().decode()  # file_id
            nx, ny = _parse_line_ints(f)
            xl, xu = _parse_line_floats(f)
            yl, yu = _parse_line_floats(f)
            zl, zu = _parse_line_floats(f)
            values = np.genfromtxt(f)

        xarr = np.linspace(xl, xu, nx)
        yarr = np.linspace(yl, yu, ny)

        # note that the indexing of WAsP grd file is 'xy' type, i.e.,
        # values.shape == (xarr.shape[0], yarr.shape[0])
        # we need to transpose values to match the 'ij' indexing
        values = values.T

        return xarr, yarr, values

    def _parse_grdfile(grdfile, regex_pattern=None, regex_var_order=None):
        match = re.findall(regex_pattern, grdfile.name)[0]
        meta = {k: v for k, v in zip(regex_var_order, match)}
        meta["var"] = _rename_var(meta["var"])

        xarr, yarr, values = _read_grd_data(grdfile)

        dims = ["west_east", "south_north", "height"]
        coords = {
            "height": [float(meta["height"])],
            "x": (("west_east",), xarr),
            "y": (("south_north",), yarr),
            "west_east": (("west_east",), xarr),
            "south_north": (("south_north",), yarr),
        }
        values = values[..., np.newaxis]

        if not meta["sector"].lower() == "all":
            dims += ["sector"]
            coords["sector"] = [int(meta["sector"])]
            values = values[..., np.newaxis]
        else:
            if meta["var"] != "site_elev":
                meta["var"] = meta["var"] + "_combined"

        da = xr.DataArray(values, dims=dims, coords=coords, name=meta["var"])

        if da.name == "site_elev":
            da = da.isel(height=0, drop=True)

        return da

    if not isinstance(grdfiles, list):
        grdfiles = [grdfiles]

    grdfiles = list(Path(f) for f in grdfiles)

    if regex_pattern is None:
        regex_pattern = r"Sector (\w+|\d+) \s+ Height (\d+)m \s+ ([a-zA-Z0-9- ]+)"

    if regex_var_order is None:
        regex_var_order = ("sector", "height", "var")

    wwc = xr.merge(
        [
            _parse_grdfile(
                grdfile, regex_pattern=regex_pattern, regex_var_order=regex_var_order
            )
            for grdfile in grdfiles
        ]
    )

    ds = update_var_attrs(wwc, _WEIB_ATTRS)
    return update_history(ds)


def read_wwc(wwc_file, crs=None):
    """Creates and validates a weibull wind climate xarray.Dataset from a netCDF File.
    it is a wrapper for xarray.load_dataset that adds windkit validation and attribute
    update.

    Parameters
    ----------
    wwc_file : str or pathlib.Path
        Path to a netCDF file that can be opened as a wwc
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`. Defaults to the embedded CRS for .nc files.

    Returns
    -------
    ds : xarray.Dataset
        weibull wind climate dataset that is formatted to match the wwc description.

    Raises
    ------
    ValueError
        If crs does not match dataset crs.
    ValueError
        If the data read is not a valid weibull wind climate dataset.
    """
    file_or_obj = Path(wwc_file)
    ext = file_or_obj.suffix
    if ext != ".nc":
        raise ValueError(f"Bwc file {wwc_file} has extension {ext} but needs to be .nc")
    ds = xr.load_dataset(file_or_obj)
    if crs is not None and not crs_are_equal(ds, crs):
        raise ValueError("Requested crs does not match dataset crs.")
    ds = update_var_attrs(ds, _WEIB_ATTRS)
    wwc_validate(ds)
    return update_history(ds)


@wwc_validate_structure_wrapper
def weibull_combined(wwc, atol=0.000001):
    """Return the all sector A & k.

    This is know as the combined weibull A and k in the
    WAsP GUI. For more information, see here:
    https://www.wasp.dk/support/faq#general__emergent-and-combined-weibull-all-sector-distributions
    Using the combined weibull A and k are calculated
    using first and third moment conservation rules.

    Parameters
    ----------
    wwc: xarray.Dataset
        Weibull Wind Climate dataset.

    Returns
    -------
    tuple of xr.DataArray
        All sector A & k DataArrays
    """
    sum1 = (wwc["wdfreq"] * weibull_moment(wwc["A"], wwc["k"], 1)).sum(
        dim="sector", skipna=False
    )
    sum3 = (wwc["wdfreq"] * weibull_moment(wwc["A"], wwc["k"], 3)).sum(
        dim="sector", skipna=False
    )
    sum1 = sum1 / wwc["wdfreq"].sum(dim="sector", skipna=False)
    sum3 = sum3 / wwc["wdfreq"].sum(dim="sector", skipna=False)

    sum_logm = np.log(sum3) / 3.0 - np.log(sum1)
    k_combined = fit_weibull_k_sumlogm(
        sum_logm, order_m_first=1, order_m_higher=3, atol=atol
    )
    A_combined = sum1 / gamma(1.0 + 1.0 / k_combined)

    return A_combined, k_combined


@wwc_validate_structure_wrapper
def wwc_mean_windspeed(wwc, bysector=False, emergent=True):
    """Calculate the mean wind speed from a weibull wind climate dataset.

    Parameters
    ----------
    wwc: xarray.Dataset
        Weibull Wind Climate dataset.
    bysector: bool
        Return results by sector or as an all-sector value. Defaults to False.
    emergent: bool
        Calculate the all-sector mean using the emergent (True) or the combined Weibull
        distribution (False). Defaults to True.

    Returns
    -------
    xarray.DataArray
        DataArray with the mean wind speed.
    """
    if bysector and emergent:
        raise ValueError(
            "Emergent wind speed cannot be calculated for sectorwise wind speed."
        )

    if emergent:
        A, k = _get_A_k(wwc, bysector=True)  # emergent always use all sectors
        return (wwc["wdfreq"] * weibull_moment(A, k, 1)).sum(dim="sector", skipna=False)
    else:
        A, k = _get_A_k(wwc, bysector=bysector)
        return weibull_moment(A, k, 1)


@wwc_validate_structure_wrapper
def wwc_power_density(wwc, air_density, bysector=False, emergent=True):
    """Calculate the power density

    Parameters
    ----------
    wwc: xarray.Dataset
        Weibull wind climate dataset.
    air_density :  float
        Air density.
    bysector: bool
        Return sectorwise mean wind speed if True. defaults to False.
    emergent: bool
        Calculate the all-sector mean using the emergent (True) or the combined Weibull
        distribution (False). Defaults to True.

    Returns
    pd : xarray.DataArray
        Data array with power density.
    """
    if bysector and emergent:
        raise ValueError(
            "Emergent power density cannot be calculated for sectorwise wind speed."
        )
    if emergent:
        A, k = _get_A_k(wwc, bysector=True)
        pd = (air_density * wwc["wdfreq"] * weibull_moment(A, k, 3.0)).sum(
            dim="sector", skipna=False
        )
    else:
        A, k = _get_A_k(wwc, bysector=bysector)
        pd = air_density * weibull_moment(A, k, 3)
    return 0.5 * pd


def wwc_to_bwc(wwc, ws_bins):
    """Creates object from directional A's and k's.

    Parameters
    ----------
    wwc: xarray.Dataset
        Weibull wind climate xr.Dataset object
    ws_bins: np.array
        Wind speed bin edges

    Returns
    -------
    bwc : xarray.Dataset
        binned wind climate from a Weibull distribution.
    """
    wwc = wwc.copy()  # make a copy to avoid modifications leaving scope

    ws_bins = xr.DataArray(ws_bins, dims=("wsbin",))
    cdfs = weibull_cdf(wwc.A, wwc.k, ws_bins)
    ws_freq = cdfs.isel(wsbin=slice(1, None)) - cdfs.isel(wsbin=slice(None, -1))
    ws_freq = ws_freq / ws_freq.sum(dim="wsbin")
    ws_freq = ws_freq.fillna(0.0)

    bwc = wwc[
        [v for v in wwc.data_vars if v not in ["A", "k"]]
    ]  # pass through other variables
    bwc["wsfreq"] = ws_freq

    wscenters = create_ws_bin_coords_from_values(ws_bins)
    bwc = bwc.assign_coords(
        {
            **wscenters.coords,
        }
    )
    bwc = update_var_attrs(bwc, _BWC_ATTRS)
    return update_history(bwc)
