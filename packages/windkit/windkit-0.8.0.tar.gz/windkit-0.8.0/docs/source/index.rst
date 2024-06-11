.. _windkit:

WindKit
=======

WindKit provides a Pythonic interface to read, write, and analyse many of the file formats used in the WAsP wind resource assessment program. Over time the project will include additional file types, and work to standardize the structures that are used in Wind Resource Assessment.

WindKit is built to include robust metadata for all objects, allowing for easier interoperability and reusability of different data sets.

.. note:: WindKit does not provide an interface to calculate WAsP results. For that you need PyWAsP, which can be purchased from the `WAsP Website <https://www.wasp.dk/products/pywasp>`_ .

Tools Using WindKit
-------------------

- Wind-validation
- New European Wind Atlas data APIs

Contact
-------

- Use the `WAsP Forum for Python Tools <https://www.wasptechnical.dk/forum/forum/19-wasp-python-tools/>`_.
- Use our support email support at wasp.dk

.. toctree::
    :caption: Setup
    :hidden:

    getting_started
    installation

.. toctree::
    :caption: Users Guide
    :hidden:

    windkit
    wind_climate_objects
    topographic_data
    wind_turbines
    plotting
    map_conversion

.. toctree::
    :caption: API
    :hidden:

    io/io

.. toctree::
    :caption: Planning
    :hidden:

    release_notes
    development_roadmap

References
----------
.. bibliography:: WAsP.bib
   :cited:
   :style: plain
