import pytest

from mtb.core.pip import VirtualEnvManager


@pytest.fixture
def manager(tmp_path):
    envs = [str(tmp_path / f"env{i}") for i in range(1, 4)]
    manager = VirtualEnvManager()

    for env in envs:
        manager.create(env)

    return manager


@pytest.mark.heavy
def test_venv_manager_initialization(manager):
    assert set(manager.envs.keys()) == {"env1", "env2", "env3"}
    assert manager._active is None


@pytest.mark.heavy
def test_create_env(manager, tmp_path):
    env_path = tmp_path / "env4"
    assert manager.create(str(env_path))
    assert env_path.stem in manager.envs


@pytest.mark.heavy
def test_activate_deactivate_env(manager):
    assert manager.activate("env1")
    assert manager._active == "env1"
    manager.deactivate()
    assert manager._active is None


@pytest.mark.heavy
def test_list_envs(manager):
    assert set(manager.list_envs()) == {"env1", "env2", "env3"}


@pytest.mark.heavy
def test_delete_env(manager):
    assert manager.delete("env1")
    assert "env1" not in manager.envs
