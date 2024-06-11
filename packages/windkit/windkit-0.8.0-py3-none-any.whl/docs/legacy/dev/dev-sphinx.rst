.. _code_documentation:

Sphinx Documentation
.....................

For documenation we are using `Sphinx <http://www.sphinx-doc.org/en/master/>`_. This is a tool that integrates well with Python, and has extensions that make it useful for documenting Fortran as well. Sphinx uses `reStructuredText <http://www.sphinx-doc.org/en/master/rest.html>`_, and requires the user to create the framework of the documentation.

We keep the documentation at two levels, the first is general documentation, such as this document, which does not depend on the source code, and provides an overview of the code. The second level is API documentation. This is provided by using `NumPy style docstrings <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`_

Please work to make sure that the documentation is updated with your changes. You can view the documentation locally by changing to the docs directory and running the make file. Typically we are focused on the HTML documentation.

.. code-block:: bash

    cd docs
    make clean
    make html

.. _docs_coverage:

Documentation Coverage
-----------------------

Much like with testing, sphinx can inspect the code to inform you about the coverage of your documentation. This can be done by running the coverage instruction of the makefile, and viewing the ``python.txt`` file.

.. code-block:: bash

    make coverage
    more build/coverage/python.txt
