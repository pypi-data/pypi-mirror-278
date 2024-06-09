"""Core functions for mtb."""

# - @mtb namespace
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

# from . import cli_tools, observer, watcher
from . import cli_tools, observer  # ,watcher
from ._utils import print_dir
from .cmd import CommandRunner
from .log import mklog, suppress_std
from .Namespace import Namespace

__all__ = [
    "CommandRunner",
    "Namespace",
    "mklog",
    "suppress_std",
    "print_dir",
    "cli_tools",
    "observer",
    "watcher",
]

__version__ = "0.0.2"
