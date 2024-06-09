import importlib, os, platform, shutil, subprocess, sys
from functools import lru_cache as cached
from pathlib import Path
from typing import List, Optional

from virtualenv import cli_run

from .context import Context, get_context
from .log import mklog


class VirtualEnvManager:
    """Class to manage Python virtual environments (virtualenv)."""

    session = None

    def __init__(self, envs: List[Path] = None):
        """
        Initialize VirtualEnvManager with the directory where virtual environments are/will be stored.

        :param venv_dir: The path to the directory for storing virtual environments.
        """
        self.log = mklog("mtb.core.pip.venv")
        self._active = None

        self.envs = {Path(env).stem: Path(env) for env in envs} if envs else {}

    def _run_command(self, args, timeout=600) -> bool:
        """Execute a shell command."""
        try:
            subprocess.run(args, timeout=timeout, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def create(self, env_path: str) -> bool:
        """Create a new virtual environment."""
        if env_path in self.envs.values():
            self.log.info(f"Virtual environment {env_path} already exists.")
            return True
        env_path = Path(env_path)
        env_name = env_path.stem
        try:
            self.log.debug(f"Creating virtual env at {env_path}")
            self.session = cli_run([str(env_path)])
            # return self.session
            self.envs[env_name] = env_path
            return True
        except Exception as e:
            self.log.error(f"Error creating virtual environment: {e}")
            return False

    def activate(self, env_name: str) -> bool:
        """Activate a virtual environment."""

        if self._active and self._active == env_name:
            self.log.info(f"Virtual environment {env_name} already active.")

        if env_name not in self.envs:
            self.log.error(
                f"Virtual environment {env_name} does not exist. You need to either create it or register it."
            )
            return False
        # Determine the appropriate subdirectory based on the operating system
        sub_directory = "Scripts" if platform.system() == "Windows" else "bin"

        # Determine the activation script
        activation_script = "activate_this.py"

        env_path = self.envs[env_name] / sub_directory / activation_script
        if env_path.exists():
            exec(env_path.read_text("utf8"), {"__file__": env_path})
            self._active = env_name
            return True
        else:
            self.log.error(
                f"Virtual environment {env_name} does not have an activation script. (looked in {env_path})"
            )
        return False

    def deactivate(self) -> None:
        """Deactivate the currently active virtual environment."""

        if "VIRTUAL_ENV" in os.environ:
            del os.environ["VIRTUAL_ENV"]

        self._active = None

    def list_envs(self) -> List[str]:
        """List all existing virtual environments."""
        return list(self.envs.keys())

    def delete(self, env_name: str) -> bool:
        """Delete a virtual environment."""

        env_path = self.envs[env_name]
        if env_path.exists() and env_path.is_dir():
            shutil.rmtree(env_path)
            del self.envs[env_name]
            return True
        return False

    def export_requirements(self, filepath: str) -> bool:
        """Export the list of installed packages in the virtual environment to a requirements file."""

        args = ["pip", "freeze", ">", filepath]
        return self._run_command(args)

    def install_from_requirements(self, filepath: str) -> bool:
        """Install packages in the virtual environment from a requirements file."""

        args = ["pip", "install", "-r", filepath]
        return self._run_command(args)

    def _ensure_env(self, env_name) -> bool:
        if not self._active and not env_name:
            self.log.error(
                "No virtual environment is currently active. You need to either activate an existing environment or specify the name of a registered environment."
            )
            return False
        if env_name:
            self.activate(env_name)
            return True

        return self._active is not None

    def install(self, package: str, env_name: str = None) -> bool:
        """Install a package in the virtual environment."""
        if not self._ensure_env(env_name):
            return False

        if isinstance(package, str):
            package = [package]

        if env_name:
            self.activate(env_name)

        args = ["pip", "install"] + package
        return self._run_command(args)

    def update_pip(self, env_name):
        if not self._ensure_env(env_name):
            return False
        self._run_command(["python", "-m", "pip", "install", "--upgrade", "pip"])


class PipManager:
    """Class to manage Python packages using Pip (using target which I highly discourage over VirtualEnvManager)."""

    def __init__(self, packages_dir: Path, log=None, context=None):
        """
        Initialize PipManager with the directory where packages are/will be stored.

        :param packages_dir: The path to the directory for storing Python packages.
        """
        self.packages_dir = Path(packages_dir)
        self.log = log or mklog("mtb.core.pip")
        self.exe_context, self.python_bin = context or get_context()
        self.pip_mapping = {
            "onnxruntime-gpu": "onnxruntime",
            "opencv-contrib": "cv2",
            "opencv-python": "cv2",
            "Pillow": "PIL",
            "protobuf": "google.protobuf",
            "PySide6-Essentials": "PySide6",
            "tb-nightly": "tensorboard",
            "qrcode[pil]": "qrcode",
            "requirements-parser": "requirements",
        }

    def _run_command(self, args, timeout=600) -> bool:
        try:
            subprocess.run(args, timeout=timeout, check=True)
            return True
        except subprocess.CalledProcessError as e:
            self.log.error(f"Command failed with error: {e}")
            return False

    def _pip_action(self, action: str, *packages, additional_flags=[]) -> bool:
        args = (
            [
                self.python_bin,
                "-m",
                "pip",
                action,
                "-t",
                self.packages_dir.as_posix(),
            ]
            + additional_flags
            + list(packages)
        )

        return self._run_command(args)

    def module_can_be_imported(self, name) -> bool:
        import_name = self.pip_mapping.get(name, name)
        try:
            importlib.import_module(import_name)
            return True
        except ModuleNotFoundError:
            return False

    def pipFound(self) -> bool:
        return self.module_can_be_imported("pip")

    def modules_can_be_imported(self, *names) -> bool:
        return all(self.module_can_be_imported(name) for name in names)

    def install_pip(self) -> bool:
        args = [self.python_bin, "-m", "ensurepip", "--user", "--upgrade", "--default-pip"]
        success = self._run_command(args)
        if success:
            self.log.success("Installed Pip")
            self.update_pip()
        return success

    def update_pip(self) -> bool:
        return self._pip_action("install", "--upgrade", "pip")

    def pip_freeze(self):
        args = [
            self.python_bin.as_posix(),
            "-m",
            "pip",
            "freeze",
            "--path",
            self.packages_dir.as_posix(),
        ]
        output = subprocess.run(
            " ".join(args),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
        )
        return output

    def install_package(self, name, force=False):
        """Install a Python package."""

        if self.module_can_be_imported(name) and not force:
            return True

        self.log.debug(f"Installing {name}")
        return self._pip_action("install", name, additional_flags=["--upgrade"])

        # args = [
        #     self.python_bin.as_posix(),
        #     "-m",
        #     "pip",
        #     "install",
        #     "-t",
        #     self.packages_dir.as_posix(),
        #     "--upgrade",
        #     name,
        # ]
        # cmd = " ".join(args)
        # process = subprocess.Popen(
        #     cmd,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE,
        #     encoding="utf-8",
        # )

        # while process.poll() != 0:
        #     line = process.stdout.readline()
        #     if not line:
        #         break
        #     print(line)

        # if not self.module_can_be_imported(name):
        #     self.handle_fatal_error(f"could not install {name}")
        #     return False

        # return True

    def handle_fatal_error(self, message):
        for line in message.splitlines():
            self.log.error(line)

    @staticmethod
    def install_packages(self, *names, force=False) -> bool:
        if not self.pipFound():
            self.install_pip()

        to_install = names if force else [n for n in names if not self.module_can_be_imported(n)]
        success = self._pip_action("install", *to_install, additional_flags=["--upgrade"])
        if success:
            self.log.success(f"Installed {' | '.join(to_install)}")
        else:
            self.handle_fatal_error(f"Could not install {to_install}")

        return success
        # if self.modules_can_be_imported(*names) and not force:
        #     return True

        # to_install = names if force else [n for n in names if not self.module_can_be_imported(n)]

        # args = [
        #     self.python_bin,
        #     "-m",
        #     "pip",
        #     "install",
        #     "-t",
        #     self.packages_dir.as_posix(),
        #     "--upgrade",
        #     *to_install,
        # ]

        # if subprocess.call(args=args, timeout=600):
        #     self.handle_fatal_error(f"could not install {to_install}")
        #     return False

        # not_found = [name for name in to_install if not self.module_can_be_imported(name)]

        # if len(not_found):
        #     print(f"Error while installing {not_found}")
        #     return False

        # self.log.success(f"Installed {' | '.join(to_install)}")
        # return True

    def install_packages_from_file(self, filepath: Path, force=False) -> bool:
        with open(filepath, "r") as f:
            packages = [line.strip() for line in f.readlines()]
        return self.install_packages(*packages, force=force)

    def uninstall_packages(self, *names) -> bool:
        """Uninstall one or multiple Python packages."""

        to_uninstall = [n for n in names if self.module_can_be_imported(n)]
        success = self._pip_action("uninstall", "-y", *to_uninstall)
        if success:
            self.log.success(f"Uninstalled {' | '.join(names)}")
        else:
            self.handle_fatal_error(f"Could not uninstall {names}")

        return success
