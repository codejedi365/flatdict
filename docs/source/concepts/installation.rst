.. _installation:

Installation
============

This package adheres to `Semantic Versioning (SemVer)`_. API changes are indicated
by the major version, non-breaking improvements by the minor version, and bug fixes
in the patch version.

.. code-block:: bash

  # Install the latest version of flatdict from PyPI
  python3 -m pip install cj365-flatdict

**RECOMMENDATION:** Pin your dependencies to the current major version to avoid
unexpected breaking changes! See the example below.

.. code-block:: toml

  # pyproject.toml
  [project]
  # ...
  dependencies = [
    "cj365-flatdict ~= 5.0"  # Adjust the version as needed
  ]

.. _Semantic Versioning (SemVer): https://semver.org/
