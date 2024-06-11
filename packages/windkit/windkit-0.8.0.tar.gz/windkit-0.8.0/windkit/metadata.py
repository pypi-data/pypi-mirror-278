# (c) 2022 DTU Wind Energy
"""
Variable Metadata for CF Conventions

This module contains a dictionary that lists all possible variables in the WindKit
system. These are then used to make metadata dictionaries for each object in their
respective modules.

In addition to the metadata, there are convience functions for updating object metadata.
"""
import inspect
import json
from datetime import datetime, timezone
from logging import Logger
from pathlib import Path

import xarray as xr

from ._version import version
from .config import CONFIG
from .data_structures import DataStructures
from .spatial._struct import get_spatial_struct

logger = Logger(__name__)

with open(Path(__file__).resolve().parent / "all_vars.json") as f:
    ALL_VARS_META = json.load(f)

_GLOBAL_CONVENTIONS = {
    "Conventions": "CF-1.8",
}


def create_coords(data, dimname, meta):
    """Create simple coordinate DataArray with metadata.

    Parameters
    ----------
    data : list or numpy.ndarray
        Data to fill the datarray with.
    dimname : str
        Name of the dimension, also name of the key in metadata dict.
    meta : dict
        dictionary containing metadata for the coordinate.

    Returns
    -------
    xarray.DataArray
        DataArray containing the coordinate.
    """
    # Create data array
    da = xr.DataArray(data, dims=dimname)
    da = da.assign_coords({dimname: da})
    da[dimname].attrs = {**meta[dimname]}

    return da


# wind time series object
_TS_ATTRS = {
    "wind_speed": ALL_VARS_META["wind_speed"],
    "wind_direction": ALL_VARS_META["wind_direction"],
    "object_type": DataStructures.TS.value,
}

# wind histogram (count) object
_HIS_ATTRS = {
    "wv_count": ALL_VARS_META["wv_count"],
    "count_bins_exceeded": ALL_VARS_META["count_bins_exceeded"],
    "object_type": DataStructures.HIS.value,
}

# stability time series object
_TS_STAB_ATTRS = {
    "temp_scale": ALL_VARS_META["temp_scale"],
}

# stability histogram object
_HIS_STAB_ATTRS = {
    "sum_temp_scale": ALL_VARS_META["sum_temp_scale"],
    "sum_squared_temp_scale": ALL_VARS_META["sum_squared_temp_scale"],
    "sum_pblh": ALL_VARS_META["sum_pblh"],
    "count_bins_exceeded": ALL_VARS_META["count_bins_exceeded"],
    "object_type": DataStructures.HIS_STAB.value,
}

# mean stability histogram
_MEAN_STAB_ATTRS = {
    "mean_temp_scale_land": ALL_VARS_META["mean_temp_scale_land"],
    "rms_temp_scale_land": ALL_VARS_META["rms_temp_scale_land"],
    "mean_pblh_scale_land": ALL_VARS_META["mean_pblh_scale_land"],
    "mean_temp_scale_sea": ALL_VARS_META["mean_temp_scale_sea"],
    "rms_temp_scale_sea": ALL_VARS_META["rms_temp_scale_sea"],
    "mean_pblh_scale_sea": ALL_VARS_META["mean_pblh_scale_sea"],
}

# mean stability histogram
_MEAN_BARO_ATTRS = {
    "mean_dgdz": ALL_VARS_META["mean_dgdz"],
    "mean_dgdz_dir": ALL_VARS_META["mean_dgdz_dir"],
}

# baroclinicity histogram object
_HIS_BARO_ATTRS = {
    "wv_count": ALL_VARS_META["wv_count"],
    "sum_dugdz": ALL_VARS_META["sum_dugdz"],
    "sum_dvgdz": ALL_VARS_META["sum_dvgdz"],
    "count_bins_exceeded": ALL_VARS_META["count_bins_exceeded"],
}


_BWC_ATTRS = {
    "wdfreq": ALL_VARS_META["wdfreq"],
    "wsfreq": ALL_VARS_META["wsfreq"],
    "meridian_convergence": ALL_VARS_META["meridian_convergence"],
    "object_type": DataStructures.BWC.value,
}


_GEOWC_ATTRS = {
    "geo_wv_freq": ALL_VARS_META["geo_wv_freq"],
    "geo_turn": ALL_VARS_META["geo_turn"],
    "object_type": DataStructures.GEOWC.value,
}


_ELEV_ROSE_ATTRS = {
    "site_elev": ALL_VARS_META["elevation"],
    "rix": ALL_VARS_META["rix"],
    "dirrix": ALL_VARS_META["dirrix"],
    "flow_sep_height": ALL_VARS_META["flow_sep_height"],
    "nray": ALL_VARS_META["bz_nray"],
    "grid": ALL_VARS_META["bz_grid"],
    "c": ALL_VARS_META["bz_c"],
    "s": ALL_VARS_META["bz_s"],
    "w": ALL_VARS_META["bz_w"],
    "hr1": ALL_VARS_META["bz_hr1"],
    "hi1": ALL_VARS_META["bz_hi1"],
    "hi2": ALL_VARS_META["bz_hi2"],
    "r": ALL_VARS_META["bz_r"],
    "object_type": DataStructures.ELEV_ROSE.value,
}

_ELEV_ROSE_COORDS = {
    "radial_dist": ALL_VARS_META["radial_dist"],
    "radials_x_radial_dist": ALL_VARS_META["radials_x_radial_dist"],
    "radials": ALL_VARS_META["radials"],
}

_ROU_ROSE_ATTRS = {
    "z0": ALL_VARS_META["rou_rose_roughness"],
    "slf": ALL_VARS_META["rou_rose_slf"],
    "dist": ALL_VARS_META["rou_rose_dist"],
    "displ": ALL_VARS_META["displacement_height"],
    "nrch": ALL_VARS_META["rou_rose_nrch"],
    "object_type": DataStructures.ROU_ROSE.value,
}

_ROU_ROSE_COORDS = {
    "max_rou_changes1": ALL_VARS_META["max_rou_changes1"],
    "max_rou_changes": ALL_VARS_META["max_rou_changes"],
}

_GEWC_ATTRS = {
    "year": ALL_VARS_META["year"],
    "max_wspd": ALL_VARS_META["max_wspd"],
    "max_wdir": ALL_VARS_META["max_wdir"],
    "max_time": ALL_VARS_META["max_time"],
    "object_type": DataStructures.GEWC.value,
}

_LINCOM_V50_ATTRS = {
    "max_wspd": ALL_VARS_META["max_wspd"],
    "max_wdir": ALL_VARS_META["max_wdir"],
    "ierror": ALL_VARS_META["lincom_lut_err"],
    "object_type": DataStructures.LINCOM_V50.value,
}

_LINCOM_V50_LUT_ATTRS = {
    "WS": ALL_VARS_META["wind_speed"],
    "WD": ALL_VARS_META["wind_direction"],
    "object_type": DataStructures.LINCOM_V50_LUT.value,
}

_LINCOM_WIND_LEVEL_ATTRS = {
    "WS": ALL_VARS_META["wind_speed"],
    "U": ALL_VARS_META["U"],
    "V": ALL_VARS_META["V"],
    "W": ALL_VARS_META["W"],
    "flow_inclination": ALL_VARS_META["flow_inclination"],
    "Z0": ALL_VARS_META["dyn_roughness"],
    "terrain_inclination": ALL_VARS_META["terrain_inclination"],
    "DU_DX": ALL_VARS_META["DU_DX"],
    "DV_DX": ALL_VARS_META["DV_DX"],
    "DW_DX": ALL_VARS_META["DW_DX"],
    "DU_DY": ALL_VARS_META["DU_DY"],
    "DV_DY": ALL_VARS_META["DV_DY"],
    "DW_DY": ALL_VARS_META["DW_DY"],
    "DU_DZ": ALL_VARS_META["DU_DZ"],
    "DV_DZ": ALL_VARS_META["DV_DZ"],
    "DW_DZ": ALL_VARS_META["DW_DZ"],
    "object_type": DataStructures.LINCOM_WIND_LEVEL.value,
}

_LINCOM_WIND_POINT_ATTRS = {
    "elevation": ALL_VARS_META["elevation"],
    "height": ALL_VARS_META["height"],
    "WS": ALL_VARS_META["wind_speed"],
    "WD": ALL_VARS_META["wind_direction"],
    "flow_inclination": ALL_VARS_META["flow_inclination"],
    "USTAR": ALL_VARS_META["USTAR"],
    "DU_DX": ALL_VARS_META["DU_DX"],
    "DV_DX": ALL_VARS_META["DV_DX"],
    "DU_DY": ALL_VARS_META["DU_DY"],
    "DV_DY": ALL_VARS_META["DV_DY"],
    "DU_DZ": ALL_VARS_META["DU_DZ"],
    "DV_DZ": ALL_VARS_META["DV_DZ"],
    "DTilt_DX": ALL_VARS_META["DTilt_DX"],
    "DTilt_DY": ALL_VARS_META["DTilt_DY"],
    "DTilt_DZ": ALL_VARS_META["DTilt_DZ"],
    "ALPHA": ALL_VARS_META["shear_exp"],
    "object_type": DataStructures.LINCOM_WIND_POINT.value,
}

_V50_GUMBEL_ATTRS = {
    "gumbel_alpha": ALL_VARS_META["gumbel_alpha"],
    "gumbel_beta": ALL_VARS_META["gumbel_beta"],
    "extreme_wspd": ALL_VARS_META["extreme_wspd"],
    "extreme_uncert": ALL_VARS_META["extreme_uncert"],
    "ierror": ALL_VARS_META["gumbel_fit_err"],
    "object_type": DataStructures.V50_GUMBEL.value,
}

# This is used by rastermap and holds all potential maptypes
_MAP_TYPE_ATTRS = {
    "elevation": ALL_VARS_META["elevation"],
    "roughness": ALL_VARS_META["roughness"],
    "landcover": ALL_VARS_META["landcover"],
    "speedup": ALL_VARS_META["cfd_speedups"],
    "turning": ALL_VARS_META["cfd_turnings"],
    "flow_inclination": ALL_VARS_META["cfd_flow_inclination"],
    "turbulence_intensity": ALL_VARS_META["cfd_turbulence_intensity"],
    "displacement_height": ALL_VARS_META["displacement_height"],
    "landmask": ALL_VARS_META["landmask"],
    "fetch": ALL_VARS_META["fetch"],
    "object_type": DataStructures.MAP_TYPE.value,
}

# this is the data structure after adding extra information to
# a basic weibull wind climate
_MET_ATTRS = {
    "A_combined": ALL_VARS_META["weib_A_combined"],
    "k_combined": ALL_VARS_META["weib_k_combined"],
    "wspd_sector": ALL_VARS_META["wind_speed_sector"],
    "wspd": ALL_VARS_META["wind_speed"],
    "wspd_combined": ALL_VARS_META["wind_speed_combined"],
    "air_density": ALL_VARS_META["air_density"],
    "power_density_sector": ALL_VARS_META["power_density_sector"],
    "power_density": ALL_VARS_META["power_density"],
    "power_density_combined": ALL_VARS_META["power_density_combined"],
    "object_type": DataStructures.MET.value,
}

_SECTOR_COORD_ATTRS = {
    "sector": ALL_VARS_META["sector"],
    "sector_ceil": ALL_VARS_META["sector_ceil"],
    "sector_floor": ALL_VARS_META["sector_floor"],
    "wind_direction": ALL_VARS_META["wind_direction"],
}

_WSBIN_COORD_ATTRS = {
    "wsbin": ALL_VARS_META["wsbin"],
    "wsceil": ALL_VARS_META["wsceil"],
    "wsfloor": ALL_VARS_META["wsfloor"],
    "wind_speed": ALL_VARS_META["wind_speed"],
}

_SPECTRUM_ATTRS = {
    "spectrum_freq": ALL_VARS_META["spectrum_freq"],
    "spectrum_power": ALL_VARS_META["spectrum_power"],
    "spec_corr_fac": ALL_VARS_META["spec_corr_fac"],
    "object_type": DataStructures.SPECTRUM.value,
}

_TOPO_EFFECTS_ATTRS = {
    "z0meso": ALL_VARS_META["z0meso"],
    "slfmeso": ALL_VARS_META["slfmeso"],
    "displ": ALL_VARS_META["displacement_height"],
    "flow_sep_height": ALL_VARS_META["flow_sep_height"],
    "user_def_speedups": ALL_VARS_META["user_def_speedups"],
    "orographic_speedups": ALL_VARS_META["orographic_speedups"],
    "obstacle_speedups": ALL_VARS_META["obstacle_speedups"],
    "roughness_speedups": ALL_VARS_META["roughness_speedups"],
    "user_def_turnings": ALL_VARS_META["user_def_turnings"],
    "orographic_turnings": ALL_VARS_META["orographic_turnings"],
    "obstacle_turnings": ALL_VARS_META["obstacle_turnings"],
    "roughness_turnings": ALL_VARS_META["roughness_turnings"],
    "dirrix": ALL_VARS_META["dirrix"],
    "site_elev": ALL_VARS_META["elevation"],
    "rix": ALL_VARS_META["rix"],
    "object_type": DataStructures.TOPO_EFFECTS.value,
}


_TOPO_CFD_EFFECTS_ATTRS = {
    "z0meso": ALL_VARS_META["z0meso"],
    "cfd_speedups": ALL_VARS_META["cfd_speedups"],
    "cfd_turnings": ALL_VARS_META["cfd_turnings"],
    "cfd_turbulence_intensity": ALL_VARS_META["cfd_turbulence_intensity"],
    "cfd_flow_inclination": ALL_VARS_META["cfd_flow_inclination"],
    "site_elev": ALL_VARS_META["elevation"],
    "object_type": DataStructures.TOPO_CFD_EFFECTS.value,
}

# this is the basic data structure returned by
# a WAsP downscaling, in WAsP GUI often referred
# to as the pwc (predicted wind climate)
_WEIB_ATTRS = {
    "A": ALL_VARS_META["weib_A"],
    "k": ALL_VARS_META["weib_k"],
    "wdfreq": ALL_VARS_META["wdfreq"],
    "object_type": DataStructures.WEIB.value,
}

_WTG_ATTRS = {
    "wind_speed": ALL_VARS_META["wind_speed"],
    "mode": ALL_VARS_META["wtg_mode"],
    "power_output": ALL_VARS_META["power_output"],
    "thrust_coefficient": ALL_VARS_META["thrust_coefficient"],
    "air_density": ALL_VARS_META["air_density"],
    "stationary_thrust_coefficient": ALL_VARS_META["stationary_thrust_coefficient"],
    "wind_speed_cutin": ALL_VARS_META["wind_speed_cutin"],
    "wind_speed_cutout": ALL_VARS_META["wind_speed_cutout"],
    "rated_power": ALL_VARS_META["rated_power"],
    "name": ALL_VARS_META["wtg_model"],
    "rotor_diameter": ALL_VARS_META["rotor_diameter"],
    "hub_height": ALL_VARS_META["hub_height"],
    "object_type": DataStructures.WTG.value,
}

# Data structure returned by aep calculations
_AEP_ATTRS = {
    "gross_AEP": ALL_VARS_META["gross_aep"],
    "gross_AEP_sector": ALL_VARS_META["gross_aep_sector"],
    "potential_AEP": ALL_VARS_META["potential_aep"],
    "potential_AEP_sector": ALL_VARS_META["potential_aep_sector"],
    "object_type": DataStructures.AEP.value,
}
# Data structure for a wind farm flow map
_WF_FLOW_MAP_ATTRS = {
    "potential_AEP_sector": ALL_VARS_META["potential_aep_sector"],
    "gross_AEP_sector": ALL_VARS_META["gross_aep_sector"],
    "AEP_deficit_sector": ALL_VARS_META["aep_deficit_sector"],
    "wspd_sector": ALL_VARS_META["wind_speed"],  # Is this right?
    "wspd_eff_sector": ALL_VARS_META["wind_speed_effective"],  # Is this right?
    "wspd_deficit_sector": ALL_VARS_META["wind_speed_deficit"],  # Is this right?
    "turbulence_intensity_eff_sector": ALL_VARS_META[
        "turbulence_intensity_effective_sector"
    ],  # there is a similar
    "wdfreq": ALL_VARS_META["wdfreq"],
    "potential_AEP": ALL_VARS_META["potential_aep"],
    "gross_AEP": ALL_VARS_META["potential_aep"],
    "AEP_deficit": ALL_VARS_META["aep_deficit"],
    "wspd": ALL_VARS_META["wind_speed"],  # Is this right?
    "wspd_eff": ALL_VARS_META["wind_speed_effective"],  # Is this right?
    "wspd_deficit": ALL_VARS_META["wind_speed_deficit"],  # Is this right?
    "turbulence_intensity_eff": ALL_VARS_META[
        "turbulence_intensity_effective"
    ],  # there is a siilar
    "object_type": DataStructures.WF_FLOW_MAP.value,
}


def _update_local_attrs(da, var_dict):
    """Updates data varaible attributes

    Parameters
    ----------
    da: xarray.DataArray
        WindKit DataArray to be updated
    vars_dict : dict
        Dictionary of attributes for the data variable

    Returns
    -------
    xarray.DataArray
        The same DataArray with updated attributes
    """
    # Update attributes if they are in the list otherwise inform the user
    try:
        da.attrs = {**da.attrs, **var_dict[da.name]}
    except KeyError as e:
        logger.info(f"KeyError{e}")

    if get_spatial_struct(da) is not None:
        da.attrs["grid_mapping"] = "crs"

    return da


def _setup_user_global_attrs():
    """
    Defines the metadata asked to the user
    """
    CONFIG.add_str("user_data", "name")
    CONFIG.add_email("user_data", "email")
    CONFIG.add_str("user_data", "institution")


def update_var_attrs(obj, var_dict):
    """Update all data variable attributes.

    Parameters
    ----------
    obj : xarray.Dataset or xarray.DataArray
        WindKit Dataset of DataArray to be updated.
    vars_dict : dict
        Dictionary maping variable names to the attributes that should be used.

    Returns
    -------
    xarray.Dataset or xarray.DataArray
        The same Dataset or DataArray with updated attributes.

    """
    _setup_user_global_attrs()
    CONFIG.create_config()
    var_dict_copy = var_dict.copy()
    object_type = var_dict_copy.pop("object_type", None)
    if isinstance(obj, xr.Dataset):
        for var in obj.data_vars:
            obj[var] = _update_local_attrs(obj[var], var_dict)
        obj.attrs["Conventions"] = "CF-1.8"
        obj.attrs["Package name"] = __name__.split(".")[0]
        obj.attrs["Package version"] = version
        obj.attrs["Creation date"] = (
            datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        )
        if object_type is not None:
            obj.attrs["Object type"] = object_type
        obj.attrs["author"] = CONFIG.get_option("user_data", "name")
        obj.attrs["author_email"] = CONFIG.get_option("user_data", "email")
        obj.attrs["institution"] = CONFIG.get_option("user_data", "institution")

    elif isinstance(obj, xr.DataArray):
        obj = _update_local_attrs(obj, var_dict)
    else:
        raise ValueError(
            "Can only add attributes to xarray.Dataset or xarray.DataArray objects."
        )

    return obj


def update_history(ds):
    """Update history global attribute.

    Updates the global history attribute for a xarray Dataset.

    Parameters
    ----------
    ds : xarray.Dataset
        WindKit Dataset to be updated.

    Returns
    -------
    xarray.Dataset
        The same Dataset with updated attribute.

    """
    current_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    package = __name__.split(".")[0]

    # Get the function call that was used before calling update_history.
    # NOTE: If call is from the python interpreter, we can't determine the context, so
    #       include a generic message.
    function_context = inspect.stack()[2].code_context
    if function_context is None:
        function_call = "Unknown python interpreter command."
    else:
        function_call = function_context[0][:-1]

    if "=" in function_call:
        function_call = function_call[function_call.index("=") + 1 :]
        if " " in function_call:
            function_call = function_call[function_call.index(" ") + 1 :]
    history_to_add = (
        current_utc + ":" + "\t" + package + "==" + version + "\t" + function_call
    )

    if "history" in ds.attrs.keys():
        ds.attrs["history"] = ds.attrs["history"] + "\n" + history_to_add
    else:
        ds.attrs["history"] = history_to_add
    return ds
