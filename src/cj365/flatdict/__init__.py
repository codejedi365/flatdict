"""
This module provides the `FlatDict` and `FlatterDict` classes for
managing nested dictionaries with flattened keys. The `FlatDict` class
allows for simple key-value storage with support for nested structures
using a specified delimiter. The `FlatterDict` class extends this
functionality to handle lists and sets as child-dict instances with
the offset as the key.
"""
# +-------------------------------------------------------------------+
# | Module: cj365.flatdict                                            |
# | Author: codejedi365, 2026                                         |
# | Licensed under the BSD-3-Clause License.                          |
# +-------------------------------------------------------------------+

from importlib.metadata import version as get_metadata_version

from cj365.flatdict.flat_dict import FlatDict
from cj365.flatdict.flatter_dict import FlatterDict

__version__ = get_metadata_version(__name__.replace("_", "-"))

__all__ = ["FlatDict", "FlatterDict"]
