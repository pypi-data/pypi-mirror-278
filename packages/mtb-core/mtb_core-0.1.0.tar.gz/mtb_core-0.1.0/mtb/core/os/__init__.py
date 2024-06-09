"""OS / FS related classes and functions.


"""
from ._base_methods import add_path, backup_file
from ._CrossPlatformPath import CrossplatformPath

__all__ = ["CrossplatformPath", "add_path", "backup_file"]
