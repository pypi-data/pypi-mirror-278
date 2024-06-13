from importlib.metadata import version

from .levels import __doc__, contains, find_path, get_level, levels, search

__version__ = version("levels")

__all__ = ["levels", "get_level", "find_path", "search", "contains"]

__doc__ = __doc__.strip()
