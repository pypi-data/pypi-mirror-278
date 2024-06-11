# (c) 2022 DTU Wind Energy
"""
Wind climate functions.
"""
import random
from itertools import product

import numpy as np

from windkit import create_dataset
from windkit.spatial import get_crs, to_point

from .binned_wind_climate import _is_bwc, bwc_power_density, bwc_ws_moment
from .data_structures import DataStructures
from .generalized_wind_climate import _is_gwc
from .geostrophic_wind_climate import _is_geowc
from .metadata import _MET_ATTRS, update_var_attrs
from .time_series_wind_climate import _is_ts
from .weibull_wind_climate import _is_wwc, wwc_mean_windspeed, wwc_power_density


def get_wc_struct(obj):
    """Get the type of a WindKit wind climate object.

    Parameters
    ----------
    obj : xarray.Dataset, xarray.DataArray
        Object to determine the wind climate structure from.

    Returns
    -------
    string :
        Spatial structure name. Can be on of:
            - 'ts'
            - 'bwc'
            - 'wwc'
            - 'genwc'
            - 'geowc'
        If no spatial structure is found None is returned.
    """
    if _is_bwc(obj):
        return DataStructures.BWC
    elif _is_wwc(obj):
        return DataStructures.WWC
    elif _is_geowc(obj):
        return DataStructures.GEOWC
    elif _is_gwc(obj):
        return DataStructures.GWC
    elif _is_ts(obj):
        return DataStructures.TS
    else:
        return None


def mean_windspeed(wco, bysector=False, emergent=True):
    """Calculate the mean wind speed from a wind climate.

    Parameters
    ----------
    wco: xarray.Dataset
        Weibull Wind Climate or Binned Wind Climate Object.
    bysector: bool
        Return results by sector or as an all-sector value. Defaults to False
    emergent: bool
        Calculate the all-sector mean using the emergent (True) or the combined Weibull
        distribution (False). Defaults to True.

    Returns
    -------
    xarray.DataArray
        DataArray with the wind speed.
    """
    # TODO: add mean wind speed of time series object
    if bysector and emergent:
        raise ValueError(
            "Emergent wind speed cannot be calculated for sectorwise wind speed."
        )
    if _is_bwc(wco):
        ws = bwc_ws_moment(wco, 1.0, bysector)
    elif emergent:
        ws = wwc_mean_windspeed(wco, bysector, emergent=True)
        ws.name = "wspd"
        return update_var_attrs(ws, _MET_ATTRS)
    else:
        ws = wwc_mean_windspeed(wco, bysector, emergent=False)

    if bysector:
        ws.name = "wspd_sector"
    else:
        ws.name = "wspd_combined"

    return update_var_attrs(ws, _MET_ATTRS)


def power_density(wco, bysector=False, emergent=True, air_density=1.225):
    """Calculate the power density of a bwc or wwc

    Parameters
    ----------
    wco: xarray.Dataset
        Weibull Wind Climate or Binned Wind Climate Object.
    bysector: bool
        Return results by sector or as an all-sector value. Defaults to False.
    emergent: bool
        Calculate the all-sector mean using the emergent (True) or the combined Weibull
        distribution (False). Defaults to True.
    air_dens: xarray.DataArray or float
        xarray.DataArray with air density with the same dimensions
        as wco, by default use US standard atmosphere air density
        of 1.225 kg/m^3

    Returns
    -------
    xarray.DataArray
        DataArray with the power density.
    """
    if bysector and emergent:
        raise ValueError(
            "Emergent power density cannot be calculated for sectorwise wind speed."
        )

    # calculate power density
    if _is_bwc(wco):
        pd = bwc_power_density(wco, bysector, air_density)
    elif emergent:
        pd = wwc_power_density(wco, air_density, bysector=False, emergent=True)
        pd.name = "power_density"
        return update_var_attrs(pd, _MET_ATTRS)
    else:
        pd = wwc_power_density(wco, air_density, bysector, emergent=False)

    if bysector:
        pd.name = "power_density_sector"
    else:
        pd.name = "power_density_combined"

    return update_var_attrs(pd, _MET_ATTRS)


def _not_equal(points):
    """Return if not a self-prediction"""
    for x, y in points:
        if x != y:
            yield (x, y)


def _higher(points):
    """Return if the target observation higher or equal than the source"""
    for x, y in points:
        if y[2] >= x[2]:
            yield (x, y)


def _in_range(points, filter_range):
    """Return if the observation is within the chosen range"""
    for x, y in points:
        bottom, top = filter_range
        if x[2] >= bottom and x[2] < top and y[2] >= bottom and y[2] < top:
            yield (x, y)


def get_cross_predictions(
    wcs,
    wcs_src=None,
    include_self_predictions=True,
    only_upward_extrapolations=True,
    filter_range=None,
    sample_size=None,
    seed=4,
):
    """Get cross predictions from a dataset

    Given the filtering options, return a dataset with the points
    where we want to predict from and where we want to predict to.

    Parameters
    ----------
    wcs: :any:`xarray.Dataset`
        wind climate `xarray.Dataset` for which we want to do cross predictions
    wcs_src: `xarray.Dataset`
        wind climate `xarray.Dataset` used as source for the cross predictions.
        If None, `wcs` is used as source and as target. Defaults to None.
    include_self_predictions: bool
        A self prediction is a pair of points where the input point is
        the exact same as the output point. Keep self predictions in the dataset?
    only_upward_extrapolations: bool
        Keep only the cross predictions where
        the height of point_in >= the height of point_out?
    filter_range: list
        height range that we want to retain from the input dataset
    sample_size: int
        Number of samples to take from the input dataset
    seed: int
        Seed number for the random sampling, if applied

    Returns
    -------
    from_locs: :any:`xr.Dataset`
        xarray dataset with input locations
    to_locs: :any:`xr.Dataset`
        xarray dataset with target locations
    """

    def point_to_multiindex(ds):
        """Convert to windkit `point` structure

        Parameters
        ----------
        ds: :any:`xr.Dataset`
            xarray dataset with windkit `point` structure

        Returns
        -------
        points: :any:`xr.Dataset`
            xarray dataset with multiindex point coordinate
        """
        pp = to_point(ds)
        return pp.set_index(point=["west_east", "south_north", "height"])

    def reindex_points(ds, locs):
        """Reindex ds by using point indices from locs

        Returns the dataset `ds` but on the points in `locs`.

        Parameters
        ----------
        ds: :any:`xr.Dataset`
            xarray dataset with windkit `point` structure
        locs: :any:`xr.Dataset`
            xarray dataset with the desired windkit `point` structure

        Returns
        -------
        points: :any:`xr.Dataset`
            xarray dataset with the variables from `ds` but at points from `locs`
        """
        points = ds.sel(
            point=locs.set_index(point=["west_east", "south_north", "height"])["point"]
        )
        return points.reset_index("point")

    point_bwc = point_to_multiindex(wcs)
    index = point_bwc.point.values
    points = ((i[0], i[1]) for i in product(index, index))

    if not include_self_predictions:
        points = _not_equal(points)

    if only_upward_extrapolations:
        points = _higher(points)

    if filter_range is not None:
        points = _in_range(points, filter_range)

    # if lp is an empty list we have filtered out all measurements
    # so we return None
    lp = list(points)
    if lp:
        if sample_size is not None:
            # take sample_size from the points, if the number of samples exceeds
            # the length of the list, take all points
            random.seed(seed)
            point_from, point_to = zip(*random.sample(lp, min(sample_size, len(lp))))
        else:
            point_from, point_to = zip(*lp)

        dataset_from = create_dataset(
            np.array(point_from).T[0],
            np.array(point_from).T[1],
            np.array(point_from).T[2],
            crs=get_crs(point_bwc),
        )
        dataset_to = create_dataset(
            np.array(point_to).T[0],
            np.array(point_to).T[1],
            np.array(point_to).T[2],
            crs=get_crs(point_bwc),
        )

        to_locs = reindex_points(point_bwc, dataset_to)

        if wcs_src is None:
            from_locs = reindex_points(point_bwc, dataset_from)
        else:
            point_wcs_src = point_to_multiindex(wcs_src)
            from_locs = reindex_points(point_wcs_src, dataset_from)

        return (from_locs, to_locs)
    else:
        return (None, None)
