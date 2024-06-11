# (c) 2022 DTU Wind Energy
"""
Create empty datasets for various WindKit structures.

The datasets have the correct shape, dimensions, coordinates and data variables and
can also be filled with meaningful random data.
"""

import numpy as np
import pandas as pd
import scipy.stats
import xarray as xr

import windkit as wk

from .metadata import (
    _BWC_ATTRS,
    _HIS_ATTRS,
    _MAP_TYPE_ATTRS,
    _MET_ATTRS,
    _TOPO_EFFECTS_ATTRS,
    _TS_ATTRS,
    _WEIB_ATTRS,
    ALL_VARS_META,
    update_history,
    update_var_attrs,
)
from .sector import create_sector_coords, create_ws_bin_coords
from .spatial import is_point, spatial_stack, spatial_unstack

_metvars_3d_nosec = [
    "wspd",  # same as A
    "power_density",  # 100 - 600
    "air_density",  # 1.225, 0.2 stddev
    "wspd_emergent",  # same as A
    "power_density_emergent",  # same as power density
    "A_combined",  # same as A
    "k_combined",  # same as k
]
_metvars_4d = ["wspd_sector", "power_density_sector"]  # same as wspd, power_density

# metadata for the generalized wind climate
_GEN_COORDS_META = {
    "gen_height": ALL_VARS_META["gen_height"],
    "gen_roughness": ALL_VARS_META["gen_roughness"],
    "sector": ALL_VARS_META["sector"],
}

__all__ = [
    "empty_wasp_site_factors",
    "empty_bwc",
    "empty_wwc",
    "empty_gwc",
    "empty_met_fields",
    "empty_z0meso",
    "empty_pwc",
    "empty_wv_count",
    "empty_raster_map",
]


def _empty_unstack(ds, is_scalar):
    """
    Allow user to retain scalar structure when using spatial_unstack"
    """
    if is_scalar:
        return ds.isel(point=0)
    else:
        return spatial_unstack(ds)


def _define_std_arrays(output_locs, nsec=12):
    """Return standard 2D, 3D, and 4D arrays in point format"""
    output_is_point = is_point(output_locs)
    out_std = spatial_stack(output_locs).drop_vars(output_locs.data_vars)
    # check if it is a scalar
    is_scalar = not output_is_point and out_std.sizes["point"] == 1

    # Setup sector
    sector_coords = create_sector_coords(nsec).coords
    dims = ("sector", "point")
    out_sec_std = out_std.assign_coords(sector_coords)
    values = np.full((nsec, out_std.sizes["point"]), np.nan, np.float32)

    out_das = {}
    # x, y
    out_das["da_2d"] = xr.DataArray(
        values[0,],
        out_std.coords,
        dims[1:],
        attrs={"_pwio_data_is_2d": True},
    )

    # sector, x, y
    out_das["da_3d_nohgt"] = xr.DataArray(
        values, out_sec_std.coords, dims, attrs={"_pwio_data_is_2d": True}
    )

    # height, x, y
    out_das["da_3d_nosec"] = xr.DataArray(
        values[0,],
        out_std.coords,
        dims[1:],
        attrs={"_pwio_data_is_2d": False},
    )

    # Sector, height, x, y
    out_das["da_4d"] = xr.DataArray(values, out_sec_std.coords, dims, attrs={})

    return out_das, out_std.attrs, is_scalar


def _copy_chunks(in_ds, out_ds):
    """copy chunks from in_ds to out_ds"""
    # If input is not chunked it will have an emtpy chunks dict, so we need to build a
    # custom chunk_map based on the chunked dimensions of the original data.
    chunk_map = {}
    for i in in_ds.chunks:
        chunk_map[i] = in_ds.chunks[i][0]

    # Remember in Python empty dictionaries are False
    if chunk_map:
        return out_ds.chunk(chunk_map)
    else:
        return out_ds


def empty_wasp_site_factors(
    output_locs,
    nsec=12,
    not_empty=True,
    site_factors=["z0meso", "displ"],
    seed=9876538,
    **kwargs,
):
    """Create empty site-factors dataset.

    Parameters
    ----------
    output_locs : xarray.Dataset
        Output geospatial information
    nsec : int
        Number of sectors. Defaults to 12.
    not_empty : bool
        If true, the empty dataset is filled with random
        meaningful data.
    site_Factors : list of strings, or string
        List of variables to include in the output, or a string "all" that
        includes all variables. Defaults to ["z0meso", "displ"]
    seed : int
        Seed for the random data, defaults to 9876538.

    kwargs : dict
        Additional arguments.

    Returns
    -------
    ds : xarray.Dataset
        Empty site factors dataset.
    """
    da_dict, unstack_attrs, is_scalar = _define_std_arrays(output_locs, nsec)

    _site_factors_vars_2d = ["site_elev", "rix"]
    _site_factors_vars_3d_nohgt = ["z0meso", "slfmeso", "displ", "dirrix"]
    _site_factors_vars_4d = [
        "user_def_speedups",
        "orographic_speedups",
        "obstacle_speedups",
        "roughness_speedups",
        "user_def_turnings",
        "orographic_turnings",
        "obstacle_turnings",
        "roughness_turnings",
    ]
    if site_factors == "all":
        site_factors = (
            _site_factors_vars_2d + _site_factors_vars_3d_nohgt + _site_factors_vars_4d
        )
    random_param_dict = {
        "z0meso": (0, 1.2),
        "slfmeso": (0, 1),
        "displ": (0, 10),
        "user_def_speedups": 1,
        "orographic_speedups": (0.6, 1.5),
        "obstacle_speedups": 1,
        "roughness_speedups": (0.6, 1.5),
        "user_def_turnings": 0,
        "orographic_turnings": (-20, 20),
        "obstacle_turnings": 0,
        "roughness_turnings": 0,
        "dirrix": (0, 0.5),
        "site_elev": (0, 100),
        "rix": (0, 0.5),
    }
    out_vars = {}
    for var in site_factors:
        if var in _site_factors_vars_2d:
            out_vars[var] = da_dict["da_2d"]
        elif var in _site_factors_vars_3d_nohgt:
            out_vars[var] = da_dict["da_3d_nohgt"]
        elif var in _site_factors_vars_4d:
            out_vars[var] = da_dict["da_4d"]
        else:
            raise ValueError(f"Unknown  {var}, cannot add to result")
    ds = xr.Dataset(
        out_vars,
        attrs=unstack_attrs,
    )

    if not_empty:
        rng = np.random.default_rng(seed)
        for val in site_factors:
            rand_param = random_param_dict[val]
            if type(rand_param) == tuple:
                ds[val].values = rng.uniform(*rand_param, ds[val].shape)
            else:
                ds[val].values = np.zeros(ds[val].shape)

    ustack_ds = _empty_unstack(ds, is_scalar)

    ds = update_var_attrs(_copy_chunks(output_locs, ustack_ds), _TOPO_EFFECTS_ATTRS)

    return update_history(ds)


def empty_tswc(output_locs, date_range=None, not_empty=True, seed=9876538):
    """
    Create empty time series wind climate dataset.

    If not_empty=True, the data variables are filled with meaninful random numbers.

    Parameters
    ----------
    output_loc : xarray.Dataset
        Output geospatial information.
    time_range : pandas.DatetimeIndex or None
        time range as a pandas DateTimeIndex. If None is passed, a default range with 100
        entries is created. Defaults to None.
    not_empty : bool
        If true, the empty dataset is filled with random
        meaningful data. Defaults to True.
    seed : int
        Seed for the random data, defaults to 9876538.

    Returns
    -------
    ds : xarray.Dataset
        Time Series wind climate dataset either empty or filled with
        random numbers.
    """

    da_dict, unstack_attrs, is_scalar = _define_std_arrays(output_locs)
    if date_range is None:
        time_values = pd.date_range(
            "2001-01-01", "2010-01-01", freq="10min", inclusive="left"
        )
    elif type(date_range) is not pd.DatetimeIndex:
        raise TypeError("date_range must be of type pandas.DatetimeIndex")
    else:
        time_values = date_range

    ds = xr.Dataset(
        {
            "wind_speed": da_dict["da_3d_nosec"],
            "wind_direction": da_dict["da_3d_nosec"],
        },
        attrs=unstack_attrs,
    )

    ds["wind_speed"] = ds["wind_speed"].expand_dims({"time": time_values})
    ds["wind_direction"] = ds["wind_direction"].expand_dims({"time": time_values})

    n_pt = len(ds["point"])
    n_timesteps = len(ds["time"])
    if not_empty:
        rng = np.random.default_rng(seed)
        k = 2.0
        A = 8.0
        ws = rng.weibull(k, size=(n_timesteps, n_pt)) * A
        wd = rng.uniform(0, 360, (n_timesteps, n_pt))

        ds["wind_speed"].data = ws
        ds["wind_direction"].data = wd

    ustack_ds = _empty_unstack(ds, is_scalar)
    ds = update_var_attrs(_copy_chunks(output_locs, ustack_ds), _TS_ATTRS)

    return update_history(ds)


def empty_bwc(output_locs, nsec=12, nbins=30, not_empty=True, seed=9876538):
    """
    Create empty binned wind climate dataset.

    If not_empty=True, the data variables are filled with meaninful random numbers,
    e.g. the sum of wdfreq is 1.

    Parameters
    ----------
    output_loc : xarray.Dataset
        Output geospatial information.
    nsec : int
        Number of sectors, defaults to 12.
    nbins: int
        Number of histogram bins, defaults to 30.
    not_empty : bool
        If true, the empty dataset is filled with random
        meaningful data.
    seed : int
        Seed for the random data, defaults to 9876538.

    Returns
    -------
    ds : xarray.Dataset
        Binned wind climate dataset either empty or filled with
        random numbers.
    """

    da_dict, unstack_attrs, is_scalar = _define_std_arrays(output_locs, nsec)
    ds = xr.Dataset(
        {"wdfreq": da_dict["da_4d"], "wsfreq": da_dict["da_4d"]}, attrs=unstack_attrs
    )
    wsbin_coords = create_ws_bin_coords(bin_width=1.0, nws=nbins)

    ds["wsfreq"] = ds["wsfreq"].expand_dims({"wsbin": wsbin_coords.values})
    ds = ds.assign_coords({**wsbin_coords.coords})
    n_pt = len(ds["point"])

    if not_empty:
        wsbin_n = np.linspace(1, nbins, nbins)
        rng = np.random.default_rng(seed)
        wsbin_full = wsbin_n.repeat(nsec * n_pt).reshape((nbins, nsec, n_pt))
        k = rng.uniform(1.5, 2.5, [nsec, n_pt])
        A = rng.uniform(5, 10, [nsec, n_pt])
        wsbin_freq_not1 = scipy.stats.weibull_min.pdf(wsbin_full, k, scale=A)
        wsbin_freq = wsbin_freq_not1 / wsbin_freq_not1.sum(0)

        ds["wsfreq"] = xr.DataArray(wsbin_freq, ds["wsfreq"].coords, ds["wsfreq"].sizes)
        ds["wdfreq"] = xr.DataArray(
            rng.dirichlet(np.ones(nsec), n_pt).T,
            ds["wdfreq"].coords,
            ds["wdfreq"].sizes,
        )

    ustack_ds = _empty_unstack(ds, is_scalar)
    ds = update_var_attrs(_copy_chunks(output_locs, ustack_ds), _BWC_ATTRS)

    return update_history(ds)


def empty_wwc(output_locs, nsec=12, not_empty=True, seed=9876538, **kwargs):
    """Create empty weibull wind climate dataset.

    If not_empty=True,the data variables are filled with meaninful random numbers, e.g.
    the values from A are generated from a uniform function between 5
    and 10 and the values for k from a uniform function between 1.5 and 2.5.

    Parameters
    ----------
    output_locs : xarray.Dataset
        Output geospatial information
    nsec : int
        Number of sectors, defaults to 12.
    not_empty : bool
        If true, the empty dataset is filled with random
        meaningful data. Defaults to True.
    seed : int
        Seed for the random data, defaults to 9876538.
    kwargs : dict
        Additional arguments.

    Returns
    -------
    ds : xarray.Dataset
        Weibull wind climate dataset either empty or filled with
        random numbers.

    """
    da_dict, unstack_attrs, is_scalar = _define_std_arrays(output_locs, nsec)

    ds = xr.Dataset(
        {"A": da_dict["da_4d"], "k": da_dict["da_4d"], "wdfreq": da_dict["da_4d"]},
        attrs=unstack_attrs,
    )
    n_pt = len(ds["point"])
    if not_empty:
        rng = np.random.default_rng(seed)
        k = rng.uniform(1.5, 2.5, [nsec, n_pt])
        A = rng.uniform(5, 10, [nsec, n_pt])
        ds["A"] = xr.DataArray(A, ds["A"].coords, ds["A"].dims)
        ds["k"] = xr.DataArray(k, ds["k"].coords, ds["k"].dims)
        ds["wdfreq"] = xr.DataArray(
            rng.dirichlet(np.ones(nsec), n_pt).T,
            ds["wdfreq"].coords,
            ds["wdfreq"].dims,
        )

    ustack_ds = _empty_unstack(ds, is_scalar)
    ds = update_var_attrs(_copy_chunks(output_locs, ustack_ds), _WEIB_ATTRS)

    return update_history(ds)


def empty_gwc(
    output_locs,
    nsec=12,
    not_empty=True,
    seed=9876538,
    gen_heights=(10.0, 50.0, 100.0),
    gen_roughnesses=(0.0, 0.03, 0.1, 0.4, 1.5),
    wdfreq_constant=False,
    **kwargs,
):
    """Create empty generalized wind climate dataset.

    If not_empty=True, the data variables are filled with meaninful random numbers, e.g.
    the values from A are generated from a uniform function between 5
    and 10 and the values for k from a uniform function between 1.5 and 2.5.

    Parameters
    ----------
    output_locs : xarray.Dataset
        Output geospatial information.
    nsec : int
        Number of sectors, defaults to 12.
    not_empty : bool
        If true, the empty dataset is filled with random
        meaningful data. Defaults to True.
    seed : int
        Seed for the random data, defaults to 9876538.
    gen_heights : list
        List of generalized heights to use for coordinates
    gen_roughnesses : list
        List of generalized roughnesses to use for coordinates
    wdfreq_constant: bool
        If True, the values of wdfreq do not change with along the dimension
        gen_heights. This is used when writing lib files. Defaults to False.
    kwargs : dict
        Additional arguments.
    Returns
    -------
    ds : xarray.Dataset
        Generalized wind climate dataset either empty or filled with
        random numbers.

    """
    da_dict, unstack_attrs, is_scalar = _define_std_arrays(output_locs, nsec)

    ds = xr.Dataset(
        {"A": da_dict["da_4d"], "k": da_dict["da_4d"], "wdfreq": da_dict["da_4d"]},
        attrs=unstack_attrs,
    )
    gen_rou_coords = np.array(gen_roughnesses, dtype=float)
    gen_h_coords = np.array(gen_heights, dtype=float)
    n_gen_rou = len(gen_rou_coords)
    n_gen_h = len(gen_h_coords)
    ds = ds.expand_dims(
        {
            "gen_roughness": gen_rou_coords,
        }
    )
    ds["A"] = ds["A"].expand_dims({"gen_height": gen_h_coords})
    ds["k"] = ds["k"].expand_dims({"gen_height": gen_h_coords})
    ds["wdfreq"] = ds["wdfreq"].expand_dims({"gen_height": gen_h_coords})

    n_pt = len(ds["point"])
    if not_empty:
        rng = np.random.default_rng(seed)
        k = rng.uniform(1.5, 2.5, [n_gen_h, n_gen_rou, nsec, n_pt])
        A = rng.uniform(5, 10, [n_gen_h, n_gen_rou, nsec, n_pt])
        ds["A"] = xr.DataArray(A, ds["A"].coords, ds["A"].dims)
        ds["k"] = xr.DataArray(k, ds["k"].coords, ds["k"].dims)
        ds["wdfreq"] = xr.DataArray(
            rng.dirichlet(np.ones(nsec), (n_gen_h, n_gen_rou, n_pt)),
            dims=("gen_height", "gen_roughness", "point", "sector"),
        )
    ds["gen_roughness"].attrs = {**_GEN_COORDS_META["gen_roughness"]}
    ds["gen_height"].attrs = {**_GEN_COORDS_META["gen_height"]}
    ds["sector"].attrs = {**_GEN_COORDS_META["sector"]}

    ustack_ds = _empty_unstack(ds, is_scalar)

    if wdfreq_constant:
        da_wdfreq_constant = ustack_ds.wdfreq.isel(gen_height=0).expand_dims(
            dim={"gen_height": ustack_ds.gen_height.values}
        )
        ustack_ds["wdfreq"] = da_wdfreq_constant

    ds = update_var_attrs(_copy_chunks(output_locs, ustack_ds), _WEIB_ATTRS)
    return update_history(ds)


def empty_met_fields(
    output_locs,
    nsec=12,
    not_empty=True,
    seed=9876538,
    met_fields=["wspd", "power_density"],
    **kwargs,
):
    """Create empty dataset filled with met_fields

    Parameters
    ----------
    output_locs : xarray.Dataset
        Output geospatial information
    nsec : int
        Number of sectors, defaults to 12
    met_fields : list of strings, or string
        List of variables to include in the output, or a string "all" with
        all the variables. Defaults to ["wspd", "power_dens"]
    kwargs : dict
        Additional arguments.
    Returns
    -------
    ds : xarray.Dataset
        empty met fields dataset
    """
    da_dict, unstack_attrs, is_scalar = _define_std_arrays(output_locs, nsec)
    random_param_dict = {
        "wspd": (5, 10),
        "power_density": (100, 600),
        "air_density": ("gaussian", 1.225, 0.2),
        "wspd_emergent": (5, 10),
        "power_density_emergent": (100, 600),
        "A_combined": (5, 10),
        "k_combined": (5, 10),
        "wspd_sector": (5, 10),
        "power_density_sector": (100, 600),
    }
    if met_fields == "all":
        met_fields = _metvars_4d + _metvars_3d_nosec

    out_vars = {}
    for var in met_fields:
        if var in _metvars_4d:
            out_vars[var] = da_dict["da_4d"]
        elif var in _metvars_3d_nosec:
            out_vars[var] = da_dict["da_3d_nosec"]
        else:
            raise ValueError(f"Unknown met_field {var}, cannot add to result")

    ds = xr.Dataset(
        out_vars,
        attrs=unstack_attrs,
    )

    if not_empty:
        rng = np.random.default_rng(seed)
        for val in met_fields:
            rand_param = random_param_dict[val]
            if len(rand_param) == 2:
                ds[val].values = rng.uniform(*rand_param, ds[val].shape)
            else:
                ds[val].values = rng.normal(*rand_param[1:], ds[val].shape)
    ustack_ds = _empty_unstack(ds, is_scalar)

    ds = update_var_attrs(_copy_chunks(output_locs, ustack_ds), _MET_ATTRS)
    return update_history(ds)


def empty_z0meso(output_locs, nsec=12, **kwargs):
    """Empty site_factors with only z0meso and slfmeso.

    Parameters
    ----------
    out_grid : xarray.Dataset
        Output geospatial information.
    nsec : int
        Number of sectors, defaults to 12.
    kwargs : dict
        Additional arguments.

    Returns
    -------
    ds : xarray.Dataset
        Empty dataset.
    """

    empty_z0 = empty_wasp_site_factors(output_locs, nsec)[["z0meso", "slfmeso"]]

    return update_history(empty_z0)


def empty_pwc(
    output_locs,
    nsec=12,
    not_empty=True,
    seed=9876538,
    met_fields=["A_combined", "k_combined", "power_density"],
    site_factors=["site_elev"],
    include_name=True,
    **kwargs,
):
    """Empty predicted wind climate with optional variables.

    Parameters
    ----------
    out_grid : xarray.Dataset
        Output geospatial information
    nsec : int
        Number of sectors, defaults to 12.
    not_empty : bool
        If true, the empty dataset is filled with random
        meaningful data. Defaults to True.
    seed : int
        Seed for the random data, defaults to 9876538.
    met_fields : list of str, string
        List of met fields variables to include in the output. If None, nothing
        is included. Defaults to A_combined, k_combined, power_density
    include_site_factors : list of str, str
        List of site factors variables to include in the output. If None, nothing
        is included. Defaults to site_elev.
    include_name : bool
        If true, include a "name" coordinate, which is a string, associated to the dimension
        point, as it is commonly seen in rsf and wrg files. Defaults to True.
    kwargs : dict
        Additional arguments.

    Returns
    -------
    ds : xarray.Dataset
        empty predicted wind climate dataset.
    """

    _, _, is_scalar = _define_std_arrays(output_locs, nsec)
    output_locs = spatial_stack(output_locs)  # needed to handle scalar case
    if include_name:
        output_locs = output_locs.assign_coords(
            name=("point", ["GridPoint"] * output_locs.sizes["point"])
        )
    ds_list = [empty_wwc(output_locs, nsec)]
    # increment seed +1
    seed += 1
    if site_factors:
        # ds_list.append(empty_wasp_site_factors(output_locs, nsec)[include_site_factors])
        ds_list.append(
            empty_wasp_site_factors(
                output_locs,
                nsec,
                site_factors=site_factors,
                seed=seed,
                not_empty=not_empty,
            )
        )
    # increment seed +1
    seed += 1
    if met_fields is not None:
        ds_list.append(
            empty_met_fields(
                output_locs,
                nsec,
                not_empty=not_empty,
                met_fields=met_fields,
                seed=seed,
            )
        )

    pwc = xr.merge(ds_list, combine_attrs="override")
    ustack_ds = _empty_unstack(pwc, is_scalar)

    # return update_history(pwc)
    return update_history(ustack_ds)


def empty_wv_count(output_locs, nsec=12, nbins=30, not_empty=True, seed=9876538):
    """
    Create empty wind vector count dataset.
    If not_empty=True, the data variables are filled with meaninful random numbers.

    Parameters
    ----------
    output_loc : xarray.Dataset
        Output geospatial information
    nsec : int
        Number of sectors, defaults to 12.
    not_empty : bool
        If true, the empty dataset is filled with random
        meaningful data, defaults to True.
    seed : int
        Seed for the random data, defaults to 9876538.

    Returns
    -------
    ds : xarray.Dataset
        Wind vector count dataset either empty or filled with
        random numbers.
    """
    da_dict, unstack_attrs, is_scalar = _define_std_arrays(output_locs, nsec)
    ds = xr.Dataset({"wv_count": da_dict["da_4d"]}, attrs=unstack_attrs)
    wsbin_coords = create_ws_bin_coords(bin_width=1.0, nws=nbins)

    ds["wv_count"] = ds["wv_count"].expand_dims({"wsbin": wsbin_coords.values})
    ds = ds.assign_coords({**wsbin_coords.coords})
    n_pt = len(ds["point"])

    if not_empty:
        rng = np.random.default_rng(seed)
        k = rng.uniform(1.5, 2.5, [nsec, n_pt])
        A = rng.uniform(5, 10, [nsec, n_pt])
        wsbin_n = np.linspace(1, nbins, nbins)
        wsbin_full = wsbin_n.repeat(nsec * n_pt).reshape((nbins, nsec, n_pt))
        scaling_fact = rng.uniform(500, 1000, [nsec, n_pt])
        wv_count_array = np.rint(
            np.multiply(
                scipy.stats.weibull_min.pdf(wsbin_full, k, scale=A),
                scaling_fact[np.newaxis, :, :],
            )
        )
        ds["wv_count"].values = wv_count_array

    ustack_ds = _empty_unstack(ds, is_scalar)
    ds = update_var_attrs(_copy_chunks(output_locs, ustack_ds), _HIS_ATTRS)

    return update_history(ds)


def empty_raster_map(output_locs, resolution, map_type="elevation"):
    """
    Create empty raster map data array The values in the raster map are a 2d
    gaussian and the boundaries are defined by output_locs.

    Parameters
    ----------
    output_locs : xarray.Dataset
        A windkit spatial object that defines the bounding box to create a raster map.
    resolution : float
        Resolution of the raster map.
    map_type : str
        Raster map type. Available options are "elevation", "roughness", or "landcover",
        defaults to "elevation.

    Returns
    -------
    raster_da : xarray.DataArray
        windkit raster map data array.
    """

    # build the raster_structure
    bb = wk.spatial.BBox.from_ds(output_locs)
    raster_ds = bb.to_grid(resolution, 10.0)  # this height is not used
    raster_da = raster_ds["output"].isel(height=0, drop=True).rename(map_type)

    # fill with a 2D gauss

    def _get_gauss(sigma, mi, x):
        return (1 / (sigma * np.sqrt(2 * np.pi))) * np.e ** (
            -0.5 * np.square((x - mi) / sigma)
        )

    sigma = 20
    mi = 0
    val = [_get_gauss(sigma, mi, x) for x in range(-50, 50 + 1, 1)]
    val = np.asarray(val)
    Amp = 25000
    for i, step in enumerate(val):
        raster_da.values[i] = Amp * val[i] * val + 1
    raster_da.values = np.round(raster_da.values)

    raster_da = update_var_attrs(raster_da, _MAP_TYPE_ATTRS)
    return update_history(raster_da)
