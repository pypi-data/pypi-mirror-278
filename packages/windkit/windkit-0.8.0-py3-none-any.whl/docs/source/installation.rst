.. _installation:

=======================
Installation
=======================

WindKit is distributed as both `pypi <https://pypi.org>`__ and `conda <https://docs.conda.io/en/latest/>`__ packages. However, due to dependencies on several GIS utilities (`GeoPandas <https://geopandas.org>`__, `Rasterio <https://rasterio.readthedocs.io>`__), which depend on large C based libraries (`GEOS <https://geos.osgeo.org/>`__, `GDAL <https://www.gdal.org/>`__, `PROJ <https://proj.org/>`__), we recommend installing using the conda packages whenever possible.

.. .. note:: If you are installing PyWAsP, which requires a license, you will obtain WindKit through DTU Wind Energy's WAsP Conda Channel instead.

Conda installation
------------------

About Conda
^^^^^^^^^^^

Conda is a package manager that is able to use many different sources of packages. WindKit's dependencies require the use of the `conda-forge <https://conda-forge.org/>`__ channel, which is a community effort to provide conda packages for a wide range of software. WindKit itself is currently only distributed through specific DTU Wind Energy channels

Instructions
^^^^^^^^^^^^

1. To install WindKit you need to first install the *conda* package manager. This is done by installing a conda based distribution. We have been using the `Mambaforge <https://github.com/conda-forge/miniforge#mambaforge>`__ distribution with great success, and recommend it, but other Conda based distributions will work as well.

2. After you have installed a conda distribution, you will need to add the DTU Wind Energy Open Conda Channel, and if not using a forge based distribution, you will also need to add the conda-forge channel.

  The easiest way to do so is via the command prompt.

  On Linux and macOS, open a terminal that has conda configured. On Windows, you will find an entry called the Anaconda Prompt, which will setup the necessary environment for configuring conda.

  Run the commands below to add the channels globally so you can use them for all conda environments::

    conda config --add channels https://conda.windenergy.dtu.dk/channel/open/
    conda config --add channels conda-forge

3. Now you can setup a new conda environment that has WindKit installed. We recommend that you always create a new environment. This helps to prevent the mixing of different channels packages, and allows for easy testing of different versions::

    conda create -n <env_name> windkit <other_libraries>


  This command will find the latest version of all of WindKit's dependencies and install them along with WindKit in an environment named *env_name*. You can add other dependencies as a space-separated list.

4. After creating the new environment, you can change to it using the *conda activate* command::

    conda activate <env_name>

Installing with pip
-------------------

WindKit can also be installed with pip, by default its plotting dependencies are not included::

  pip install windkit

To install with plotting dependencies use::

  pip install windkit[plots]

As noted above, you may run into issues with using the pip installer, please see the installation instructions for `GeoPandas <https://geopandas.org/en/stable/getting_started/install.html>`__ and `Rasterio <https://rasterio.readthedocs.io/en/latest/installation.html>`__ to find the best installation method for your platform.

Dependencies
------------

Required dependencies:

  - `dtu_config <https://pypi.org/project/dtu-config/>`__
  - `geopandas <https://geopandas.org>`__ (version 0.8 or later)
  - `lxml <https://lxml.de/>`__
  - `netcdf4 <https://unidata.github.io/netcdf4-python/>`__
  - `numpy <http://www.numpy.org/>`__
  - `packaging <https://packaging.pypa.io/en/latest/>`__ (Provides version handling)
  - `pandas <http://pandas.pydata.org/>`__ (version 1 or later)
  - `pyproj <https://github.com/pyproj4/pyproj>`__ (version 2.2.2 or later)
  - `rasterio <https://rasterio.readthedocs.io>`__
  - `rtree <https://github.com/Toblerity/rtree>`__
  - `scipy <https://scipy.org/>`__
  - `shapely <https://shapely.readthedocs.io/en/stable/manual.html>`__
  - `xarray <xarray.pydata.org/>`__

Plotting dependencies (optional):
  - `kaleido <https://pypi.org/project/kaleido/>`__ (Used to export plotly images to file)
  - `matplotlib <https://matplotlib.org/>`__
  - `plotly <https://plotly.com/python/>`__

Optional dependencies:
  - `numba <https://numba.pydata.org/>`__ (Used to speed up some functions)
  - `earthengine-api <https://developers.google.com/earth-engine/guides/python_install>`__ (Google Earth Engine: provides access to geospatial data from google. Non-commercial uses only.)
  - `planetary-computer <https://pypi.org/project/planetary-computer/>`_ (Microsoft Planetary Computer: provides access to geospatial and atmospheric data from Microsoft. Terms of use apply.)
  - `pystac-client <https://pystac-client.readthedocs.io/en/stable/>`_ (Used to access SpatioTemporal Asset Catalogs (STAC) data on Microsofts Planetary Computer)
  - `fsspec <https://filesystem-spec.readthedocs.io/en/latest/>`_ (Used for accessing ERA5 data from the Planetary Computer)
  - `adlfs <https://pypi.org/project/adlfs/>`_ (Used for accessing ERA5 data from the Planetary Computer)
