import os, subprocess
from pathlib import Path, _posix_flavour, _windows_flavour
from typing import Dict, Optional, Union


class CrossplatformPath(Path):
    """
    A class that manages paths specific to different operating systems and inherits from pathlib.Path.

    Supports paths for Windows, MacOS, Linux, and a default 'all' path.
    """

    _flavour_map = {
        "win32": _windows_flavour,
        "darwin": _posix_flavour,
        "linux": _posix_flavour,
    }

    def __new__(
        cls, all: str = None, win: str = None, macos: str = None, linux: str = None, *args, **kwargs
    ):
        # Set the flavour for the Path object based on OS
        cls._flavour = cls._flavour_map[os.sys.platform]

        current_os = os.sys.platform
        specific_path = {
            "win32": win,
            "darwin": macos,
            "linux": linux,
        }.get(current_os, all)

        if specific_path:
            specific_path = os.path.expandvars(specific_path)
        else:
            specific_path = os.path.expandvars(all)

        self = super().__new__(cls, specific_path, *args, **kwargs)
        self._set_all_os_paths(all, win, macos, linux)
        return self

    def _set_all_os_paths(self, all: str, win: str, macos: str, linux: str):
        self._paths = {
            "all": all,
            "win32": win,
            "darwin": macos,
            "linux": linux,
        }

    def get(self, os_name: str = None) -> Path:
        """Retrieve the path for a specific OS."""
        os_name = os_name or os.sys.platform
        pth = self._paths.get(os_name) or self._paths.get("all")
        print("USING PATH: ", pth)
        if pth is None:
            raise ValueError(f"No path for OS {os_name}")

        return Path(os.path.expandvars(pth))

    def ensure_dir(self) -> None:
        """Ensure the path exists as a directory. If not, create it."""
        self.mkdir(parents=True, exist_ok=True)

    def reveal(self):
        """
        Open the path in the OS's file explorer.
        """
        current_os = os.sys.platform

        if current_os == "win32":
            subprocess.run(["explorer", str(self)])
        elif current_os == "darwin":
            subprocess.run(["open", str(self)])
        elif current_os == "linux":
            # Trying to open with the default file explorer (assuming GNOME/Nautilus here).
            # More logic can be added for other desktop environments if needed.
            subprocess.run(["nautilus", str(self)]).returncode == 0 or subprocess.run(
                ["xdg-open", str(self)]
            )
        else:
            raise NotImplementedError(f"Reveal for platform '{current_os}' is not implemented.")
