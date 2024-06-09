"""
Tests for CommandRunnner and Observer
"""
import logging

import pytest

from mtb.core.cmd import CommandRunner
from mtb.core.observer import Observer

# This gets the root logger
logger = logging.getLogger()

# Sets the level to debug, meaning it will capture all logging messages from DEBUG level and up
logger.setLevel(logging.DEBUG)


@pytest.mark.asyncio
async def test_multiple_commands():
    logger.info("running complex test")

    async def test_observer(self, stream_name, line):
        logging.debug(f"Test observer called: {stream_name}, {line}")

        if stream_name == "stdout":
            assert line in ["Hello", "World", "Another stdout line"]
        elif stream_name == "stderr":
            assert line in ["Error", "Another stderr line"]

    my_observer = Observer()
    my_observer.update = test_observer

    logger.info("Spawned observer")

    runner = CommandRunner()
    runner.subscribe(my_observer)
    logger.info("Subscribed command to observer")

    await runner.run_command("echo Hello && echo Error 1>&2")
    await runner.run_command("echo World && echo Another stderr line 1>&2")
    await runner.run_command("echo Another stdout line")

    stdout, stderr = await runner.get_output()
    assert set(stdout) == set(["Hello", "World", "Another stdout line"])
    assert set(stderr) == set(["Error", "Another stderr line"])


@pytest.mark.asyncio
async def test_successful_command():
    logger.info("running test 01")

    async def test_observer(self, stream_name, line):
        logging.debug(f"Test observer called: {stream_name}, {line}")

        if stream_name == "stdout":
            assert line == "Hello"
        elif stream_name == "stderr":
            assert line == "Error"

    my_observer = Observer()
    my_observer.update = test_observer

    logger.info("Spawned observer")

    runner = CommandRunner()
    runner.subscribe(my_observer)
    logger.info("Subscribed command to observer")

    await runner.run_command("echo Hello")

    stdout, stderr = await runner.get_output()
    assert stdout == ["Hello"]
    # assert stderr == ["Error"]


def nottest_successful_command():
    logger.info("running test 02")

    runner = CommandRunner()
    runner.run_command("echo hello")
    stdout, stderr = runner.get_output()
    assert stdout == ["hello"]
    assert stderr == []
