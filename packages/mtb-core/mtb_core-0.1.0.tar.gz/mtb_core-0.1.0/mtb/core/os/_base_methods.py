#!/usr/bin/env python3
import os, shutil, sys, uuid
from pathlib import Path
from typing import List, Optional, Union

from mtb.core.log import mklog

log = mklog(__name__)


def add_path(path: Union[str, Path, List[Union[str, Path]]], prepend: bool = False) -> None:
    """
    Adds a given path, or list of paths, to Python's sys.path.

    Behavior:
    - If `path` is a list of paths, each one is added recursively.
    - If `path` is an instance of Path, it is resolved to its absolute string representation.

    Uniqueness:
    - The function ensures that no duplicate paths are added, irrespective of case.

    Position:
    - If `prepend` is True, the path is added at the beginning of sys.path.
    - Otherwise, it is added at the end.

    Args:
        path (Union[str, Path, List[Union[str, Path]]]): The path or list of paths to add to sys.path.
        prepend (bool, optional): Whether to add the path at the beginning. Defaults to False.
    """

    if isinstance(path, list):
        for p in path:
            add_path(p, prepend)
        return

    if isinstance(path, Path):
        path = str(path.resolve())

    normalized_path = os.path.normpath(path.lower())
    normalized_sys_path = [os.path.normpath(p.lower()) for p in sys.path]

    if normalized_path not in normalized_sys_path:
        if prepend:
            sys.path.insert(0, path)
        else:
            sys.path.append(path)


def backup_file(
    fp: Path,
    target: Optional[Path] = None,
    backup_dir: str = ".bak",
    suffix: Optional[str] = None,
    prefix: Optional[str] = None,
):
    """
    Creates a backup of a given file, optionally specifying target directory and filename modifiers.

    Location Rules:
    - If `target` is provided, the backup will be created there.
    - Otherwise, if `suffix` or `prefix` are specified, backup is created in `(parent of fp) / (backup_dir) / (prefix)_(stem)_(suffix)`.
    - If neither `target` nor `suffix`/`prefix` are provided, backup is created in `(parent of fp) / (backup_dir) / (stem)_(uuid)`.

    Directory Handling:
    - If the target directory does not exist, it is created.

    Overwrite Rules:
    - If the target backup file already exists, a new backup with a UUID is created alongside it.

    Args:
        fp (Path): The file path of the file to be backed up.
        target (Optional[Path], optional): Explicit target directory for the backup. Defaults to None.
        backup_dir (str, optional): Name of the backup directory if `target` is not specified. Defaults to ".bak".
        suffix (Optional[str], optional): Suffix to append to the backup filename. Defaults to None.
        prefix (Optional[str], optional): Prefix to prepend to the backup filename. Defaults to None.

    Raises:
        FileNotFoundError: If the source file specified in `fp` does not exist.
    """
    if not fp.exists():
        raise FileNotFoundError(f"No file found at {fp}")

    backup_directory = target or fp.parent / backup_dir
    backup_directory.mkdir(parents=True, exist_ok=True)

    stem = fp.stem

    if suffix or prefix:
        new_stem = f"{prefix or ''}{stem}{suffix or ''}"
    else:
        new_stem = f"{stem}_{uuid.uuid4()}"

    backup_file_path = backup_directory / f"{new_stem}{fp.suffix}"

    # Perform the backup
    shutil.copy(fp, backup_file_path)
    log.debug(f"File backed up to {backup_file_path}")

    return backup_file_path
