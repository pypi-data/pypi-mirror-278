import sys

from .diseases_tree import DiseaseTree, get_all_children, get_all_parents, get_subtree
from .utils import plot_tree

__all__ = [
    "DiseaseTree",
    "get_all_children",
    "get_all_parents",
    "plot_tree",
    "get_subtree",
]

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "label-tree"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
