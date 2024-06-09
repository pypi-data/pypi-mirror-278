import asyncio, shutil, tempfile, uuid
from pathlib import Path

import aiofiles

from mtb.core import mklog

log = mklog(__name__)


class PathFixtures:
    async def __aenter__(self):
        log.debug("Async entering context manager")
        self.base_dir = Path(tempfile.mkdtemp())

        log.debug(f"Created base directory: {self.base_dir}")
        return self

    # def __init__(self):
    #     self.base_dir = Path(tempfile.mkdtemp())

    async def create_dummy_file(
        self, parent_folder, name=None, content=None, content_template="{content}"
    ):
        file_name = name or f"{uuid.uuid4()}.txt"
        file_path = parent_folder / file_name
        content = content or content_template.format(content=str(uuid.uuid4()))
        async with aiofiles.open(file_path, "w") as f:
            await f.write(content)
        return file_path

    # async def create_dummy_folder(self, name):
    #     folder_path = self.base_dir / name
    #     folder_path.mkdir()
    #     return folder_path

    async def create_dummy_folder(self, parent_folder):
        folder_name = str(uuid.uuid4())
        folder_path = parent_folder / folder_name
        folder_path.mkdir()
        return folder_path

    async def create_complex_hierarchy(self, parent_folder, depth=3, branching_factor=2):
        if depth == 0:
            log.warning("Reached depth 0, no more folders to create")
            return

        log.debug(
            f"Creating folder at {parent_folder} (depth {depth}, branching factor {branching_factor})"
        )
        folder_creation_tasks = []
        file_creation_tasks = []

        for _ in range(branching_factor):
            new_folder = await self.create_dummy_folder(parent_folder)
            log.debug(f"Created folder: {new_folder}")
            folder_creation_tasks.append(
                self.create_complex_hierarchy(new_folder, depth - 1, branching_factor)
            )
            file_creation_tasks.append(self.create_dummy_file(new_folder))

        await asyncio.gather(*folder_creation_tasks, *file_creation_tasks)

    def cleanup(self):
        # Remove base_dir and all its contents
        shutil.rmtree(self.base_dir)

    async def __aexit__(self, exc_type, exc_value, traceback):
        log.debug("Async exiting context manager")

        self.cleanup()
