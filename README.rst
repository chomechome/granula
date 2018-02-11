Granula: Multi-file Configurations for Python Applications
==============================================

.. image:: https://travis-ci.org/chomechome/granula.svg?branch=master
    :target: https://travis-ci.org/chomechome/granula
    :alt: TravisCI status

---------------

**Granula** is a tool that aims to help maintain multi-file configurations for
Python applications (with environments and more).

Installation
------------

::

    $ pipenv install granula

or, in a more familiar way to some (though you should take a look at `pipenv <http://pipenv.readthedocs.io/en/latest/>`)

    $ pip install granula

🌈🌈🌈

Features
----------

- Gathers configurations from multiple files or directories.
- Supports widely used file formats (YAML, JSON).
- Offers a small DSL that allows to load environment variables into config
files.
- Manages different configuration environments (e.g. testing, production).

Usage
-------

.. code-block:: python

    >> config = granula.Config.from_directory('examples/multi-file/settings')
    >> config
    Config({'name': 'Darth Vader', ...})
    >> config.name
    'Darth Vader'
    >> config.occupation
    'sith lord'
    >> config.family
    Config({'fiancee': 'Padme Amidala', 'children': ['Luke', 'Leia']})

where ``examples/multi-file/settings`` is a directory that contains multiple
configuration files.

``granula.Config.from_directory`` parses files in the lexicographic order.
Every file is expected to contain a mapping. The values specified in the
preceding files can be overwritten in the succeeding files
(``config.name`` in the example above).

``granula.Config.from_directory`` takes a ``pattern`` parameter which is used
to match filenames. If a string is passed, it is considered to be a shell-style
wildcard pattern. An object that implements ``granula.pattern.IFilenamePattern``
can also be passed. See ``examples/environments/`` on how to manage
configuration environments using ``pattern`` parameter.

Also see ``examples/dsl/`` for examples on how to load environment variables in
config files using ``granula`` DSL.
