.. _topographic_data:

Topographic Data
================

Topographic data in WindKit comes in two formats, vector `vector_map` and raster `raster_map`, and is stored with two variables of interest, elevation and land-cover, sometimes known as land-use.

.. note:: Roughness data is automatically converted to land-cover data in WindKit.

Geospatial Data Structures
--------------------------

Vector Data
^^^^^^^^^^^

Vector data represents objects as points, lines, or polygons, and is the data that you are used to working with in WAsP, which treats elevation as contours and uses change lines to identify areas of different roughness. Vector data is stored in memory using the `geopandas.GeoDataFrame` objects, which allows you to apply many common GIS functions to the data.

WindKit's vector_map functions work with the common `WAsP .map (WAsP) <https://gdal.org/drivers/vector/wasp.html#vector-wasp>`_ file format, as well as many other common GIS formats. We have relied mostly on custom `Geography Markup Language (GML) <https://gdal.org/drivers/vector/gml.html>`_ formats for data exchange with WAsP and the WAsP Map Editor, but recommend using `GeoPackage (GPKG) <https://gdal.org/drivers/vector/gpkg.html#vector-gpkg>`_ for working with GIS programs or when working exclusively with WindKit.

.. table:: Vector data I/O mapping
   :widths: auto
   :align: center

   ====== ========== ==========
   Format Elevation  Land-cover
   ====== ========== ==========
   .map    rw (wasp) ro
   .gml    ro        rw (wasp)
   .gpkg   rw        ro
   ====== ========== ==========

Raster Data
^^^^^^^^^^^

Raster data is data that is on a regular grid, which in WindKit means that it is made up of square pixels, i.e. dx is equal to dy. The data may be either in projected or geographic space, but each pixel contains a value of the variable that the object stores.

Many online resources, such as SRTM elevation or the `Copernicus Global Land Cover <https://doi.org/10.5281/zenodo.3243509>`_, provide data in raster format. WindKit has been extensively tested using the `Golden Software ASCII Grid (.grd) <https://gdal.org/drivers/raster/gsag.html>`_ and `GeoTIFF (.tif) <https://gdal.org/drivers/raster/gtiff.html>`_ file formats, but most GIS formats should work. Raster data is stored in memory using xarray.DataArrays, and has some GIS functionality added using the `Rasterio <https://rasterio.readthedocs.io/en/latest/>`_ library.

Topographic Variables
---------------------

Elevation
^^^^^^^^^

Elevation describes the height of the surface of the Earth above sea level. It is also common called terrain data, or orography data. It is commonly stored in raster format, but is also stored as contour lines (lines of equal value) in the vector representation.

Atmospheric Roughness Data
^^^^^^^^^^^^^^^^^^^^^^^^^^

Atmospheric roughness data is a proxy for the aerodynamic roughness of a surface. It is defined as the height at which the wind speed reaches 0 m/s. In WindKit, we do not define this data directly, but instead rely on a combination of land-cover maps, and LandCoverTables to determine the value of this field.

Land-cover Data
^^^^^^^^^^^^^^^

Land-cover data describes the surface of the land in broad descriptive categories. For example, you may list the land as urban, cropland, or forest.

In WindKit, land-cover maps are used in place of atmospheric roughness maps. These maps are also able to be used in WAsP since 12.7. Instead of storing the roughness value directly on the lines, land-cover change lines use integer IDs to identify the land-cover class of a region, this is then combined with a `LandCoverTable` to get the necessary aerodynamic fields. This allows additional data, including displacement height, to be used in flow calculations, to provide improved descriptions of the land surface. However, it also means that for roughness data you will need to keep track of both your map, which specifies where the categories of the data are located, and the `LandCoverTable`, which specifies the relevant data for each category of land-cover.

Topographic Data Download
-------------------------

WindKit provides an interface to the `Google Earth Engine
<https://earthengine.google.com/>`_ and `Microsofts Planetary Computer <https://planetarycomputer.microsoft.com/>`_, through the :py:func:`windkit.get_map` function, which provides several land cover and elevation datasets for download.

.. note:: To acces the Earth Engine Platform, :py:func:`windkit.get_map` relies on the  `earthengine-api
    <https://developers.google.com/earth-engine/guides/python_install>`_, which is an optional dependency and needs to be installed if you wish to use this functionality.

    Additionally you will need to sign up for a Google Account, and accept their terms of service for the Google Earth Engine.

    Similarly, to access Microsofts Planetary Computer Platform, you will need to install the optional dependencies `planetary-computer <https://pypi.org/project/planetary-computer/>`_ and `pystac_client <https://pystac-client.readthedocs.io/en/stable/>`_.

    Please read the terms of service for both platforms before using download and using data from these platforms.

    `Earth Engine Terms of service <https://earthengine.google.com/terms/>`_

    `Microsofts Planetary Computer terms of service <https://planetarycomputer.microsoft.com/terms>`_
