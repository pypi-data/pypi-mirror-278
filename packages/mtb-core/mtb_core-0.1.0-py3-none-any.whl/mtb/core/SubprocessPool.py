import asyncio, subprocess
from concurrent.futures import ThreadPoolExecutor


class SubprocessPoolException(Exception):
    """Base exception for all subprocess pool errors."""

    pass


class TaskFailureException(SubprocessPoolException):
    """Raised when a task fails and early_fail is True."""

    pass


class Signal:
    def __init__(self):
        self._subscribers = []

    def connect(self, func):
        self._subscribers.append(func)

    def emit(self, *args, **kwargs):
        for subscriber in self._subscribers:
            subscriber(*args, **kwargs)


class Task:
    def __init__(self, command):
        self.command = command
        self.on_done = Signal()
        self.on_failure = Signal()
        self.on_std_out = Signal()
        self.on_std_err = Signal()


class SubprocessPool:
    def __init__(self, max_concurrent=4, early_fail=False):
        self.max_concurrent = max_concurrent
        self.tasks = []
        self.early_fail = early_fail
        self.executor = ThreadPoolExecutor(max_concurrent)
        self.futures = []

    def add_task(self, command):
        task = Task(command)
        self.tasks.append(task)
        return task

    def run_subprocess(self, task):
        cmd = task.command.replace('"', '\\"')
        process = subprocess.Popen(
            f'''nu -c "{cmd}"''',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )

        for line in process.stdout:
            task.on_std_out.emit(line.strip())

        process.wait()
        if process.returncode == 0:
            task.on_done.emit(task)
        else:
            task.on_failure.emit(task)
            if self.early_fail:
                self.cancel()  # Cancel remaining tasks if early_fail is True
                raise TaskFailureException(f"Task {task.command} failed, aborting pool.")

        err = process.stderr.read().strip()
        if err:
            task.on_std_err.emit(err)

    def run(self):
        for task in self.tasks:
            future = self.executor.submit(self.run_subprocess, task)
            self.futures.append(future)

    def cancel(self):
        for future in self.futures:
            future.cancel()
