import os, sys
from pathlib import Path

import pytest

from mtb.core.os import CrossplatformPath, add_path, backup_file

# Mock environment variables for testing purposes.
os.environ["USERPROFILE"] = "C:\\Users\\TestUser"
os.environ["HOME"] = "/home/testuser"


# region CrossPlaftormPath
@pytest.fixture
def path_data(tmp_path):
    return {
        "all": str(tmp_path / "universal" / "path"),
        "win": str(tmp_path / "win" / "path"),
        "linux": str(tmp_path / "ubuntu" / "path"),
    }


def test_cross_initialization(path_data):
    paths = CrossplatformPath(all=path_data["all"])
    assert str(paths) == path_data["all"]


def test_ensure_dir_method(path_data):
    path = CrossplatformPath(all=path_data["all"])
    path.ensure_dir()

    assert path.exists()
    assert path.is_dir()


def test_inherited_pathlib_methods(path_data, tmp_path):
    path = CrossplatformPath(all=path_data["all"])

    # Test `joinpath`
    new_path = path.joinpath("subdir")
    assert new_path.as_posix() == (Path(path_data["all"]) / "subdir").as_posix()

    # Test `parent`
    assert path.parent.as_posix() == (tmp_path / "universal").as_posix()

    # Test `name`
    assert path.name == "path"

    # Test `suffix`
    assert path.suffix == ""


def test_get_method_for_different_os(path_data):
    paths = CrossplatformPath(all=path_data["all"], win=path_data["win"], linux=path_data["linux"])

    assert str(paths.get("win32")) == path_data["win"]
    assert str(paths.get("linux")) == path_data["linux"]
    assert (
        paths.get("darwin").as_posix() == Path(path_data["all"]).as_posix()
    )  # MacOS path not set, so it defaults to 'all'


# endregion


# region add_path
def test_add_path_single(tmp_path):
    p = tmp_path / "test_single"
    p.mkdir()
    add_path(p)

    assert os.path.normpath(str(p)) in sys.path


def test_add_path_list(tmp_path):
    p1 = tmp_path / "test1"
    p1.mkdir()
    p2 = tmp_path / "test2"
    p2.mkdir()
    add_path([p1, p2])
    assert str(p1) in sys.path
    assert str(p2) in sys.path


def test_add_path_prepend(tmp_path):
    p = tmp_path / "test_prepend"
    p.mkdir()
    add_path(p, prepend=True)
    assert sys.path[0] == str(p)


# endregion


# region backup_file
def test_backup_file_target(tmp_path):
    src = tmp_path / "file.txt"
    src.write_text("test")
    tgt = tmp_path / "backup"
    tgt.mkdir()
    backup_path = backup_file(src, target=tgt)

    assert backup_path.exists()
    assert backup_path.parent == tgt


def test_backup_file_suffix_prefix(tmp_path):
    src = tmp_path / "file.txt"
    src.write_text("test")
    backup_path = backup_file(src, suffix="_suffix", prefix="prefix_")
    assert backup_path.exists()


def test_backup_file_default(tmp_path):
    src = tmp_path / "file.txt"
    src.write_text("test")
    backup_path = backup_file(src)

    assert backup_path.exists()
    assert backup_path.parent == tmp_path / ".bak"
    assert backup_path.name.startswith("file_")
    assert backup_path.name.endswith(".txt")


def test_backup_file_nonexistent(tmp_path):
    src = tmp_path / "nonexistent.txt"
    with pytest.raises(FileNotFoundError):
        backup_file(src)


# endregion
