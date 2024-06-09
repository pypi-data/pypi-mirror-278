import asyncio, signal, subprocess, threading
from asyncio.subprocess import PIPE, STDOUT
from contextlib import suppress
from pathlib import Path

# from queue import Empty, Queue
from typing import Any, List, Union

from .log import mklog
from .observer import Observable, Observer

log = mklog(__name__)


class CommandOutputObserver(Observer):
    def update(self, observable, *args, **kwargs):
        stdout_line, stderr_line = args
        if stdout_line:
            print(f"stdout: {stdout_line}")
        if stderr_line:
            print(f"stderr: {stderr_line}")


class CommandRunner(Observable):
    def __init__(self):
        self.interrupted_event = threading.Event()
        super().__init__()
        self.stdout_queue = asyncio.Queue()
        self.stderr_queue = asyncio.Queue()

        self.stdout_lines = []
        self.stderr_lines = []

        log.debug("CommandRunner created")

    async def get_output(self):
        return self.stdout_lines, self.stderr_lines

    async def run_command(self, cmd: Union[str, List[Any]]):
        """Execute a shell command and asynchronously read its output.

        Args:
            cmd (Union[str, List]): Command to run.

        Raises:
            ValueError: If the 'cmd' argument is neither a string nor a list.
        """
        # signal.signal(signal.SIGINT, self._handle_interrupt)
        log.debug(f"Running command: {cmd}")

        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        await asyncio.gather(
            self._read_stream(process.stdout, self.stdout_queue, "stdout"),
            self._read_stream(process.stderr, self.stderr_queue, "stderr"),
        )

    async def _read_stream(self, stream, queue, stream_name):
        lines = self.stdout_lines if stream_name == "stdout" else self.stderr_lines
        while True:
            line = await stream.readline()
            if line:
                line = line.decode("utf-8").strip()
                queue.put_nowait(line)
                lines.append(line)  # Append the line to appropriate list
                log.debug(f"Notifying observers: {stream_name}, {line}")

                await self.notify_async(stream_name, line)
                log.debug("Notified observers")
            else:
                break

    # region private

    def _prepare_shell_cmd(self, cmd: Union[str, List[str]]) -> str:
        """Prepare the shell command from input."""
        if isinstance(cmd, str):
            return cmd
        elif isinstance(cmd, list):
            return " ".join(arg.as_posix() if isinstance(arg, Path) else str(arg) for arg in cmd)
        else:
            raise ValueError("Invalid 'cmd' argument. It must be a string or a list of arguments.")

    # endregion


class SimpleObserver(Observer):
    def update(self, observable, *args, **kwargs):
        stdout, stderr = asyncio.run(observable.get_output())
        print("New update:")
        print("STDOUT:", stdout)
        print("STDERR:", stderr)


# runner = CommandRunner()
# runner.run_command("ls -la")

# runner = CommandRunner()
# runner.run_command("ls -la")
# runner.run_command("ls -la")
