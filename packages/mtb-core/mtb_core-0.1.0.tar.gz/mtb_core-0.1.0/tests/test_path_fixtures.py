import os

import pytest

from mtb.core.fixtures import PathFixtures


@pytest.mark.asyncio
async def test_create_dummy_file():
    async with PathFixtures() as fixtures:
        parent_folder = fixtures.base_dir
        dummy_file = await fixtures.create_dummy_file(parent_folder)
        assert dummy_file.exists()
        assert dummy_file.is_file()


@pytest.mark.asyncio
async def test_create_dummy_folder():
    async with PathFixtures() as fixtures:
        parent_folder = fixtures.base_dir
        dummy_folder = await fixtures.create_dummy_folder(parent_folder)
        assert dummy_folder.exists()
        assert dummy_folder.is_dir()


@pytest.mark.asyncio
async def test_create_complex_hierarchy():
    async with PathFixtures() as fixtures:
        parent_folder = fixtures.base_dir
        depth = 2
        branching_factor = 2
        await fixtures.create_complex_hierarchy(parent_folder, depth, branching_factor)

        expected_dir_count = sum(branching_factor**i for i in range(depth + 1))
        expected_file_count = sum(branching_factor**i * branching_factor for i in range(depth))

        # Count actual directories and files
        actual_dir_count = 1  # root folder is not created by `create_complex_hierarchy`
        actual_file_count = 0

        for dirpath, dirnames, filenames in os.walk(parent_folder):
            actual_dir_count += len(dirnames)
            actual_file_count += len(filenames)

        # Verifications
        assert (
            actual_dir_count == expected_dir_count
        ), f"Expected {expected_dir_count} directories, got {actual_dir_count}"
        assert (
            actual_file_count == expected_file_count
        ), f"Expected {expected_file_count} files, got {actual_file_count}"


@pytest.mark.asyncio
async def test_cleanup():
    async with PathFixtures() as fixtures:
        base_dir = fixtures.base_dir
    assert not base_dir.exists()
