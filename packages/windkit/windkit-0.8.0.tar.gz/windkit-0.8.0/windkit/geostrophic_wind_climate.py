# (c) 2022 DTU Wind Energy
"""Geostrophic wind climate module

A geostrophic wind climate is somehwat similar as a binned wind climate, but
contains two variables: the geo_wv_freq and geo_turn. geo_wv_freq is the frequency
binned by wind speed and wind direction, where the whole histogram sums to 1 (note
that in a binned wind climate the frequency in one sector sums to one).

A valid geostrophic wind climate therefore has dimensions ``sector`` and ``wsbin``
and variables ``geo_wv_freq`` and ``geo_turn``. Also it must have a valid spatial
structure.
"""
from ._errors import WindClimateValidationError
from ._validate import create_validator

DATA_VAR_DICT_GEOWC = {
    "geo_wv_freq": ["wsbin", "sector"],
    "geo_turn": ["wsbin", "sector"],
}

REQ_DIMS_GEOWC = ["wsbin", "sector"]

REQ_COORDS_GEOWC = [
    "south_north",
    "west_east",
    "height",
    "sector",
    "wsbin",
    "crs",
]

geowc_validate_structure, geowc_validate_structure_wrapper = create_validator(
    DATA_VAR_DICT_GEOWC,
    REQ_DIMS_GEOWC,
    REQ_COORDS_GEOWC,
    checks_iterator=[],
)


def _is_geowc(wco):
    """Check if a wind climate is a geostrophic wind climate

    Returns true if geowc and false if not

    Parameters
    ----------
    wco: xarray.Dataset
        Wind Climate Object

    Returns
    -------
    Bool
        Returns true if geowc and false if not
    """
    try:
        geowc_validate_structure(wco)
        return True
    except WindClimateValidationError:
        return False
