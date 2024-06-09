from pathlib import Path

import pytest

from mtb.core.patcher import apply_patches, hash_function


# Example method to patch into pathlib.Path
def super_parent(self, level):
    out = self
    for _ in range(level):
        out = out.parent
    return out


@pytest.fixture
def setup_patches():
    yield {
        ("pathlib.Path",): {
            "super_parent": super_parent,
        }
    }


def test_patch_enable(setup_patches):
    apply_patches(setup_patches, True)

    assert hasattr(Path, "super_parent")


def test_patch_disable(setup_patches):
    apply_patches(setup_patches, True)
    apply_patches(setup_patches, False)

    assert not hasattr(Path, "super_parent")


def test_discern_patched(setup_patches):
    apply_patches(setup_patches, True)

    assert hasattr(Path, "super_parent")

    assert hasattr(Path.super_parent, "_patched")

    assert Path.super_parent._patched == True


def test_no_unintended_override(setup_patches):
    from PySide6.QtCore import QPoint  # Dynamic import just like in patch_qt

    def new_method(self):
        print("Something new")
        return self

    original_hash = hash_function(Path.as_posix)

    setup_patches[("pathlib.Path",)]["as_posix"] = new_method
    with pytest.raises(RuntimeError):
        apply_patches(setup_patches, True)

    # Check that the original method is not overridden
    assert hash_function(Path.as_posix) == original_hash


def test_patched_result(setup_patches):
    apply_patches(setup_patches, True)
    assert hasattr(Path, "super_parent")

    here = Path(__file__)
    ground = here.parent.parent.parent
    ours = here.super_parent(3)

    assert ground == ours
