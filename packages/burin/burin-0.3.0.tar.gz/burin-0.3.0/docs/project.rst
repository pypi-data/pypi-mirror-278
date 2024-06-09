===================
Project Information
===================

--------------------
Package Installation
--------------------

Burin is available on `PyPI <https://pypi.org/project/burin/>`_ and can be
installed using any Python package manager such as ``pip``.

Burin does not have any dependencies and is purely Python, so it should be
usable in almost any CPython environment from version 3.7 - 3.12.  It may also
work with other Python implementations, but has not been tested.

--------------
Git Repository
--------------

Burin is open-source and the main repository is hosted on `Github
<https://github.com/PeacefullyDisturbed/burin>`_.

If you have questions or suggestions they can be discussed through the
project's `discussion board
<https://github.com/PeacefullyDisturbed/burin/discussions>`_.  Though if you
encounter any issues please create an issue on the project's `issue
tracker <https://github.com/PeacefullyDisturbed/burin/issues>`_.

Any pull requests should adhere to the same general style of the existing code
base and pass all current linting rules and tests configured on the project.

-------------
Documentation
-------------

Burin's documentation is hosted on `Read the Docs
<https://burin.readthedocs.io/>`_.

The documentation source is avaialble in the repository and can be built using
`Sphinx <https://www.sphinx-doc.org/en/master/index.html>`_.

--------------
Build and Test
--------------

Burin uses `Hatch <https://hatch.pypa.io>`_ to manage environments, task
running, and building for development.

All tests use `PyTest <https://docs.pytest.org>`_ and can be run using the
'test' environment defined in the Hatch configuration within the pyproject.toml
file.

`Ruff <https://docs.astral.sh/ruff/>`_ is used for linting and also configured
through the pyproject.toml file.
