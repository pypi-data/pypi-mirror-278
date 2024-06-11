.. |deg| unicode:: U+00B0 # Degree symbol

.. module:: windkit

.. _windkit_api:

WindKit API
==============

The ``windkit`` module contains several modules for reading and writing WAsP specific files, as well as performing common geospatial operations on these datasets. These are split into three groups, wind climate data, topographic data, and geospatial tools. You can find an introduction to each of these areas below.

.. _wind_climate_data_api:

Wind Climate objects
--------------------

WAsP works with a number of different :ref:`wind_climates`, which each have their own API. All wind climates have an ``xarray.Dataset`` backend that can be used to provide wind specific calculations.

.. autosummary::
    :toctree: wc_autogen

    time_series_wind_climate
    binned_wind_climate
    generalized_wind_climate
    weibull_wind_climate

.. _wind_climate_tools_api:

Wind Climate tools
------------------

Tools to work with windkit wind climate objects.

.. autosummary::
    :toctree: wct_autogen

    sector
    weibull
    wind
    wind_climate
    wind_data

.. _topographic_data_api:

Topographic Data
----------------

:ref:`topographic_data` provides the roughness and elevation data that is used to model the wind resource. The tools in WindKit allow you to work with both raster and vector based maps, and use the powerful GDAL library behind the scenes to enable a wide variety of file formats to be used.



.. autosummary::
    :toctree: topo_autogen

    vector_map
    raster_map
    elevation_map
    roughness_map
    landcover
    windkit.get_map
    map_conversion.lines2poly
    map_conversion.poly2lines


.. _geospatial_tools_api:

Geospatial Tools
----------------

The WindKit Geospatial Tools allow you to perform common GIS functions such as convert between the different :ref:`geospatial_structures`, reproject or warp the data into common projections, and clip or mask the data based on additional data sources.

In addition to the provided tools, since WindKit stores its objects in the formats of powerful python libraries, you can also make use of additional `geopandas <https://geopandas.org/>`_ functions for vector data, and additional `xarray <http://xarray.pydata.org>`_ functions for raster data.

Throughout this documentation, the following abbreviations are used to reference different data types.

* geodf - either a `geopandas.GeoDataFrame` or `geopandas.GeoSeries`
* xr_data - either an `xarray.DataArray` or `xarray.Dataset`
* CRS - `pyproj.crs.CRS`

.. autosummary::
    :toctree: spatial_autogen

    spatial
    spatial.BBox
    spatial.add_crs
    spatial.get_crs
    spatial.crs_are_equal
    spatial.mask
    spatial.reproject
    spatial.clip
    spatial.warp
    spatial.create_dataset

.. _plotting_api:

Plotting
--------

WindKit Plotting allows you to execute a number of different plotting functions in order to visualize and analyze your data. Plots are largely broken into two categories; statistical and maps. Statistical plots are generally plotted using Plotly and Dash Python libraries at a single location, e.g. mast or turbine location, while maps use `geopandas <https://geopandas.org/>`_ and `xarray <http://xarray.pydata.org>`_ functions directly to show an overview of the area.


.. autosummary::
    :toctree: plot_autogen

    plot
    plot.histogram
    plot.histogram_lines
    plot.operational_curves
    plot.raster_plot
    plot.roughness_rose
    plot.time_series
    plot.vertical_profile
    plot.wind_rose
    plot.color
    plot.landcover_map

.. _wind_turbine_api:

Windkit's wind turbine API has routines to load both wind turbine generator power curves, and to create layouts of wind farms.

.. autosummary::
    :toctree: wind_turbine_autogen

    wind_turbine_generator
    wind_turbines

.. _ltc_api:

Long Term Correction
--------------------

Windkit allows to perform long term correction for wind time series using linear regresion or the variance ratio method.

.. autosummary::
    :toctree: ltc_autogen

    ltc.mcp
    ltc.regression
    ltc.scores

.. _other_data_api:

Other data
----------

Additional windkit functions.

.. autosummary::
    :toctree: other_autogen

    empty
    workspace

.. _metadata_handling_api:

Metadata handling
-----------------

Functions to handle metadata.

.. autosummary::
    :toctree: metadata_autogen

    metadata
