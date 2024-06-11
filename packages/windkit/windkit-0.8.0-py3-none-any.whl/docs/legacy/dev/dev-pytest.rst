.. _unit_testing:

Pytest
......

The development of RAM software relies on several levels of testing. For the Pungi environment this requires the unit testing of all python modules. By unit testing the Python API, we also cover a fair amount of the Fortran code that is included in the environment.

For Python unit testing we have selected `pytest <https://docs.pytest.org/en/latest/>`_. While Python has an included unit testing module [unittest], we have found that the simplicity of pytest and the ability to include compact tests is worth relying on the 3rd party module.

All tests should be in the separate ``test`` directory, and it is recommended that you install packages you are working on in :ref:`install_develop`.

You can run the existing tests from the ``test`` directory using the command::

    pytest

If you get an error with 'module not found' it is worth running pytest from the root directory
instead with (see here:https://stackoverflow.com/questions/10253826/path-issue-with-pytest-importerror-no-module-named-yadayadayada)::

    python -m pytest test/

Pytest searches for tests in the current directory by default following a few simple rules:

- recurse through all directories
- search for files named either ``test_*.py`` or ``*_test.py`` (we recommend the first for RAM software)
- Functions or methods are identificed as tests if they include the  ``test_`` prefix, or if methods are inside of a ``Test`` prefixed class.

It is important to add tests when errors are found to make sure that the errors do not return in later revisions of the code.

.. _test_coverage:

Testing Coverage
----------------

We are aiming for 100% coverage on all python modules, this can be tested using `pytest-cov <https://pypi.python.org/pypi/pytest-cov>`_. Pytest-cov produces coverage reports by comparing all path routes in a module and coparing it with the tests that are used. When you commit your code, the CI sytem automatically runs the command below, to list all missing code routes in the pywasp Package.

.. code-block:: bash

    py.test --cov-report term-missing:skip-covered --cov=pywasp

When working on a module, please add any missing tests before creating a merge request.
