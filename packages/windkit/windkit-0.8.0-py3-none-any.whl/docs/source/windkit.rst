.. _windkit_intro:

WindKit Introduction
====================

The WindKit library is a utility library that contains routines for reading and writing WAsP file formats. WindKit builds on the powerful `xarray <http://xarray.pydata.org/en/stable/>`_ library, which provides an interface for N-D labeled arrays and datasets. Xarray provides an in-memory representation of a NetCDF file, allowing us to work with spatial-temporal data in an easy to use way.
In addition to providing a wide range of I/O functionality, WindKit provides plotting routines using the `Plotly library  <https://plotly.com/python/>`_, which provides rich interactive plots viewable in any web browser. Also many common functions are provided.

Today, WindKit is designed to allow you to view and interact with WAsP's input and and output files to analyze your results, and to provide a common API for reading and writing these files in Python. By providing this package for free, we hope that other tools that read and write these files will use this package allowing for standardization across the wind resource assessment community.

.. .. note:: If you wish to perform WAsP calculations, you will need to install the `PyWAsP <http://docs.wasp.dk/pywasp/>`_ package, which requires a `PyWAsP license <http://www.wasp.dk/products>`_.

Input/Output formats
--------------------

WindKit provides reading support for all WAsP formats, including the legacy (*.tab*, *.lib*, *.rsf*, and *.map*) file formats, modern (*.owc*, *.gwc*, and *.gml*) formats, and WindKit NetCDF (*.nc*) and GeoPackage (*.gpkg*) based formats. WindKit can also read data from a WAsP Workspace.

You can write your data to the *.tab*, *.lib*, *.rsf*, and *.nc* formats for wind climates. For vector maps, you can write to the *.map* or *.gpkg* formats, while land-cover maps can be written to the *.gml* or *.gpkg* formats.

Xarray integration
------------------

Rather than using classes for WindKit's internal objects, most of the structures are stored in xarray Datasets. This enables us to support a flexible structure, scaling from single point, single height data to large regional areas with data at at multiple heights. However, to support this functionality we require a set of core-dimensions, which means that your dimension variables have to have specific names for the scripts to work correctly.

.. _core_coordinates:

Core coordinates
^^^^^^^^^^^^^^^^

In xarray terminology, coordinates are fields that are intended to label points in the data variables of the object. In the most simple use case, they are 1-D arrays that label the positions of a given dimension. This allows you to access the data not just though integer lookup, but through the actual values of the coordinates themselves.

In WindKit, we rely on a few core coordinates, that require specific names.

The majority of the core coordinates relate to the geospatial dimensions of the data, ``south_north`` and ``west_east``. These names were chosen as your data could either be in geographical (latitude, longitude) or projected (x, y) space. Additionally, all objects must have a ``crs`` coordinate, which defines the geospatial projection of the data. This is stored in the xarray object as a set of attributes on the coordinate, using the PyProj package conversion from GIS projection information to `NetCDF CF <http://cfconventions.org/Data/cf-conventions/cf-conventions-1.8/cf-conventions.html#grid-mappings-and-projections>`_ projection information. Geospatial data is a core part of WindKit, and therefore, there is an entire sub-package (`windkit.spatial`) dedicated to it.

The vertical coordinate must be called ``height``, and refers to the height above the elevation surface. This can be thought of as the boom height of a mast, or the hub-height of a wind turbine.

Instead of wind directions, WAsP works with wind direction sectors, which are binned sets of wind directions. In WindKit, this coordinate is called ``sector`` and, as is the WAsP convention, wind direction sectors start in the North (0°) and progress clockwise. Wind direction sectors are always identified by their central degree, so the North sector in a 12-sector file would cover the area from (-15° to 15°).

.. _geospatial_structures:

Geospatial structures
^^^^^^^^^^^^^^^^^^^^^

In addition to the coordinate names, WindKit supports four different spatial structures, these relate to the actual dimensions of your data. Each of these types could be useful for different purposes. Throughout this documentation, you will see ``...`` as dimensions, this consists of optional dimensions, which could include ``sector``, but not any of the other core dimensions.

1. point
    Point data has the least structure of any of the Geospatial structures, it consists a single dimension ``(..., point)`` that can have different ``south_north``, ``west_east``, and ``height`` coordinates at each location. Therefore, each of the coordinates will be 1-D arrays of dimension ``(point)``.

2. stacked point
    Stacked Point data, may relate to e.g. a set of met masts, that all have the same boom heights. In Stacked Point data, the ``south_north`` and ``west_east`` coordinates have dimension ``(stacked_point)``, while the height coordinate has its own dimension ``(height)``. This means that all ``x, y`` points in the dataset are expected to have data at all heights.

3. raster
    Raster data corresponds to data in the form of the GIS raster, i.e. a set of 2-D planes. In WindKit, the the ``south_north`` and ``west_east`` coordinates must be linearly increasing, and they each have their own dimension.

4. cuboid
    Cuboid data is a special case of raster data, where the ``height`` dimension is also specified. This is the most common format for raster data in WindKit, with the more general raster data format only being used for map data.
