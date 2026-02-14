from importlib.metadata import version as get_metadata_version

from cj365.flatdict.flat_dict import FlatDict
from cj365.flatdict.flatter_dict import FlatterDict

__version__ = get_metadata_version(__name__.replace("_", "-"))

__all__ = ["FlatDict", "FlatterDict"]
