.. _developers:

=======================
Developer Information
=======================

For developing in the DTU RAM software system, several convenience tools are required in addition to the standard windkit installation. Make sure you have looked at the developer notes in :ref:`install_develop`.

This guide will give you an overview of the
practices relied on for developing RAM software, individual tools may have additional practices that you can find in their documentation.


=======================
Developer Installation
=======================

If you are developing and need to work with documentation and testing you should use :program:`pip` to install the following packages:

.. note:: We need use sphinx <1.7.0 to be able to build fortran docs.

.. code-block:: bash

  pip install sphinx==1.6.7 sphinx_rtd_theme sphinx-argparse pytest pytest-cov

To build the documentation you will also need to install graphviz, on Linux this is best done through your package manager.

Install WindKit
................

windkit is then installed using distutils.

.. code-block:: bash

  python setup.py install

.. _install_develop:

Development mode
-----------------

If you are a developer you may wish to install WindKit in `development mode <http://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode>`_. Development mode creates a .egg-link file in your deployment directory that links to the project source code rather than installing the software. This means that your changes are automatically available. This is particularly powerful when combined with :ref:`unit_testing` so that you can update and test your new code without having to reinstall the package.

.. code-block:: bash

  python setup.py develop # Developer mode
