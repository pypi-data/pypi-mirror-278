import pytest

from mtb.core.pip import PipManager


@pytest.fixture
def tmp_venv_dir(tmpdir):
    return tmpdir.mkdir("venv")


@pytest.fixture
def pip_manager(tmp_venv_dir):
    return PipManager(tmp_venv_dir)


def test_virtual_env_and_install(tmp_venv_dir):
    # (pip_manager: PipManager,)
    pass
    # Test PipManager functionalities inside the virtual environment
    # assert pip_manager.module_can_be_imported("sys") == True
    # assert pip_manager.install_package("requests") == True
    # assert pip_manager.install_package("requirements-parser") == True


# def test_module_can_be_imported(pip_manager):
#     assert pip_manager.module_can_be_imported("sys") == True


# def test_install_package(pip_manager):
#     assert pip_manager.install_package("requests") == True


# def test_uninstall_packages(pip_manager):
#     assert pip_manager.uninstall_packages("requests") == True
