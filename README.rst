Granula: Multi-file Configurations for Python Applications
==============================================

.. image:: https://img.shields.io/pypi/v/granula.svg
    :target: https://pypi.python.org/pypi/granula
    :alt: Package version

.. image:: https://img.shields.io/pypi/l/granula.svg
    :target: https://pypi.python.org/pypi/granula
    :alt: Package license

.. image:: https://img.shields.io/pypi/pyversions/granula.svg
    :target: https://pypi.python.org/pypi/granula
    :alt: Python versions

.. image:: https://travis-ci.org/chomechome/granula.svg?branch=master
    :target: https://travis-ci.org/chomechome/granula
    :alt: TravisCI status

.. image:: https://codecov.io/github/chomechome/granula/coverage.svg?branch=master
    :target: https://codecov.io/github/chomechome/granula
    :alt: Code coverage

---------------

**Granula** is a tool that aims to help maintain multi-file configurations for
Python applications (with environments and more).

Installation
------------

::

    $ pipenv install granula

or just use pip (though you should definitely take a look at `pipenv <https://pipenv.readthedocs.io/en/latest/>`_)

🌈🌈🌈

Features
----------

- Gathers configurations from multiple files or directories.
- Supports widely used file formats (YAML, JSON).
- Offers a small DSL that allows to load environment variables into config files.
- Manages different configuration environments (e.g. testing, production).

Usage
-------

Create a config object from a directory with multiple configuration files:

.. code-block:: python

    >> import granula
    >> config = granula.Config.from_directory('examples/multi-file/settings')
    >> config
    Config({'name': 'Darth Vader', ...})
    >> config.name
    'Darth Vader'
    >> config.family
    Config({'fiancee': 'Padme Amidala', 'children': ['Luke Skywalker', 'Leia Organa']})

Files are parsed in lexicographic order. The values specified in the preceding files can be overwritten in the succeeding files.

Do the same in a recursive manner:

.. code-block:: python

    >> config = granula.Config.from_directory(..., recursive=True)

Match YAML files using filename pattern:

.. code-block:: python

    >> config = granula.Config.from_directory(..., pattern=granula.Extension('yaml'))

Do the same with a shell-style wildcard pattern:

.. code-block:: python

    >> config = granula.Config.from_directory(..., pattern=granula.Wildcard('*.yaml'))

Match configuration files for different environments:

.. code-block:: python

    >> testing = granula.Config.from_directory('examples/environments/settings', pattern=granula.Environment('testing'))
    >> production = granula.Config.from_directory('examples/environments/settings', pattern=granula.Environment('production'))

Combine patterns in arbitrary ways:

.. code-block:: python

    >> config = granula.Config.from_directory(..., pattern=granula.All(granula.Environment('testing'), granula.Extension('yaml')))

Load environment variables into config files using a DSL, for example, in YAML:

.. code-block::

    variable: ${env VARIABLE}

Do the same with a default value:

.. code-block::

    variable: ${env VARIABLE | val 10}
