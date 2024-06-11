.. _wind_climates:

Wind Climate Objects
====================

As described in the :ref:`windkit_intro`, WindKit relies on specifically structured xarray datasets in addition to classes to store data in memory. Below you will find out about the different types of objects that are present in WindKit.

.. _time_series_wind_climate:

Time Series Wind Climate
------------------------

The `time_series_wind_climate` (**twc**) contains a time series of ``wind speed`` and ``wind direction``. It is a the most basic wind climate from which all others can be derived. It also is the largest of the wind climates retaining all of the original information.

In addition to the :ref:`core_coordinates`, **twc** objects also contain the dimension ``time``, which identifies the time of the given wind data.

Creating a `xarray.Dataset` object in the **twc** format is quite simple using the `xarray.Dataset` constructor. The following example creates a **twc** object with three heights and 100 hours of data.


.. ipython:: python

    import numpy as np
    import pandas as pd
    import xarray as xr

    tswc = xr.Dataset(
        data_vars=dict(
            wind_speed = xr.DataArray(np.random.rand(100, 3)*10, dims=['time', 'height']),
            wind_direction = xr.DataArray(np.random.rand(100, 3)*360, dims=['time', 'height']),
        ),
        coords=dict(
            time = (("time",), pd.date_range('2020-01-01', periods=100, freq='h')),
            height = (("height"), [10, 50, 100]),
        )
    )
    print(tswc)

To add the spatial information to the dataset you can add a new dimension using `xarray.Dataset.expand_dims`.
The projection can be added using the :py:func:`windkit.spatial.add_crs` function. In this case, where we already have a height coordinate,
and we want to add the x and y coordinates, we call the point dimension ``stacked_point``.

.. ipython:: python

    import windkit as wk

    tswc = (
        tswc
        .expand_dims("stacked_point")
        .assign_coords(
            west_east = (("stacked_point",), [10.0]),
            south_north = (("stacked_point",), [56.0]),
        )
    )

    tswc = wk.add_crs(tswc, crs=4326)
    tswc

Windkit provides a function to create a **twc** object from a `pandas.DataFrame` object using the
:func:`windkit.read_timeseries_from_pandas` function. The `pandas.DataFrame` should have a time index,
the coordinate and projection should be added as in the previous example,
and the columns of wind speed and direction needs to associated with heights as in the following example.

.. ipython:: python

    data = {
        "wind_speed_10m": np.random.rand(100)*10,
        "wind_speed_50m": np.random.rand(100)*10,
        "wind_speed_100m": np.random.rand(100)*10,
        "wind_direction_10m": np.random.rand(100)*360,
        "wind_direction_50m": np.random.rand(100)*360,
        "wind_direction_100m": np.random.rand(100)*360,
    }

    df = pd.DataFrame(
        data,
        index=pd.date_range('2020-01-01', periods=100, freq='h'),
    )

    print(df)

    west_east, south_north = 10.0, 56.0
    crs = 4326

    height_to_columns = {
        10: ("wind_speed_10m", "wind_direction_10m"),
        50: ("wind_speed_50m", "wind_direction_50m"),
        100: ("wind_speed_100m", "wind_direction_100m"),
    }

    tswc = wk.read_timeseries_from_pandas(
        df,
        west_east,
        south_north,
        crs=4326,
        height_to_columns=height_to_columns,
    )
    tswc

The result is the same as the previous example.


Binned Wind Climate
--------------------

The `binned_wind_climate` (**bwc**) contains a histogram representation of the wind, for different wind direction sectors. Historically these have been used for encoding observational data, and in WAsP Observed Wind Climate is used for this type of data. However there is no reason that they couldn't be used for other wind data as well. In WAsP, these are stored in ".tab" and ".owc" files, which can be read using WindKit.

In addition to the :ref:`core_coordinates`, **bwc** objects also contain the dimension ``wsbin``, which identifies the wind speed bins of the histogram. Wind speed bins are characterized by their upper boundary, e.g. a wind speed bin from 0-1 would be identified with a wind speed value of 1.

In addition to reading **bwc**'s from files, you can create them from weibull distributions and time-series data.

Creating a **bwc** `xarray.Dataset` from numpy arrays can be done like this:

.. ipython:: python

    wsbins = np.linspace(0.0, 30.0, 31)
    wdbins = np.linspace(-15.0, 345.0, 13)

    wsfreq = np.random.rand(30, 12)
    wsfreq = wsfreq / wsfreq.sum(axis=0)

    wdfreq = np.random.rand(12)
    wdfreq = wdfreq / wdfreq.sum()

    bwc = xr.Dataset(
        data_vars=dict(
            wsfreq=(("wsbin", "sector"), wsfreq),
            wdreq=(("sector",), wdfreq),
        ),
        coords=dict(
            wsbin=(("wsbin",), (wsbins[1:] + wsbins[:-1]) / 2.0),
            wsfloor=(("wsbin",), wsbins[:-1]),
            wsceil=(("wsbin",), wsbins[1:]),
            sector=(("sector",), (wdbins[1:] + wdbins[:-1]) / 2.0),
            sector_floor=(("sector_floor",), np.mod(wdbins[:-1], 360)),
            sector_ceil=(("sector_ceil",), np.mod(wdbins[1:], 360)),
        )
    )
    bwc

See the `time_series_wind_climate`_ section for how to add the spatial information to the dataset.



Generalized Wind Climate
------------------------

A Generalized Wind Climate is a key part of the WAsP Methodology. The `generalized_wind_climate` (**gwc**) contains the wind in a virtual world, where there is no terrain and there are homogeneous roughness values, i.e. no roughness changes. Generalized wind climates are represented as Weibull distributions (scale [A]; shape [k]) and sector-wise frequency values. Because the **gwc** exists in a virtual world, it contains several additional dimensions compared to the other wind climate files. ``gen_height`` is the height above the constant terrain in the generalized atmosphere, and ``gen_roughness`` is the homogeneous roughness length. In WAsP, you were limited to exactly five of each of these parameters, however in WindKit you can use as many or as few as you wish.

WindKit provides the ability to create **gwc** objects from ".lib" and ".gwc" files. This is used

Creating a **gwc** `xarray.Dataset` manually can be done like this:

.. ipython:: python


    gen_heights = np.array([10, 25, 50, 100, 200])
    gen_roughnesses = np.array([0.0, 0.03, 0.1, 0.3, 1.5])

    A = np.random.rand(5, 5, 12) * 10
    k = np.random.rand(5, 5, 12) + 1
    wdfreq = np.random.rand(5, 5, 12) * 360.0

    gwc = xr.Dataset(
        data_vars=dict(
            A=(("gen_height", "gen_roughness", "sector"), A),
            k=(("gen_height", "gen_roughness", "sector"), k),
            wdfreq=(("gen_height", "gen_roughness", "sector"), wdfreq),
        ),
        coords=dict(
            gen_height=(("gen_height",), gen_heights),
            gen_roughness=(("gen_roughness",), gen_roughnesses),
            sector=(("sector",), (wdbins[1:] + wdbins[:-1]) / 2.0),
            sector_floor=(("sector_floor",), np.mod(wdbins[:-1], 360)),
            sector_ceil=(("sector_ceil",), np.mod(wdbins[1:], 360)),
        )
    )
    gwc

Remember to add spatial information to the dataset as described in the `time_series_wind_climate`_ section.


Weibull Wind Climate
--------------------

The `weibull_wind_climate` (**wwc**) is related to the `Binned Wind Climate`_, but instead of a histogram,
it is represented solely as the weibull parameters for the different sectors.
In WAsP, this was often stored as ".rsf" files, which can be read from WindKit.
These are the objects that most often store the results of a WAsP simulation.

This is how you create a **wwc** `xarray.Dataset` manually:

.. ipython:: python

    A = np.random.rand(12) * 10
    k = np.random.rand(12) + 1
    wdfreq = np.random.rand(12) * 360.0

    wwc = xr.Dataset(
        data_vars=dict(
            A=(("sector",), A),
            k=(("sector",), k),
            wdfreq=(("sector",), wdfreq),
        ),
        coords=dict(
            sector=(("sector",), (wdbins[1:] + wdbins[:-1]) / 2.0),
            sector_floor=(("sector_floor",), np.mod(wdbins[:-1], 360)),
            sector_ceil=(("sector_ceil",), np.mod(wdbins[1:], 360)),
        )
    )
    wwc
