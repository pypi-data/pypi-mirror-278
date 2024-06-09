import logging

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class _FileWatcher(FileSystemEventHandler):
    def __init__(self, callback, file_extension):
        self.callback = callback
        self.file_extension = file_extension

    def on_modified(self, event):
        try:
            if event.src_path.endswith(self.file_extension):
                logging.debug(f"File {event.src_path} modified.")
                self.callback()
        except Exception:
            logging.exception("An exception occurred in on_modified.")


class Watcher:
    def __init__(self, path, callback, file_extension=".txt"):
        self.observer = Observer()
        self.handler = _FileWatcher(callback, file_extension)
        self.observer.schedule(self.handler, path=path, recursive=False)

    def start(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def join(self):
        self.observer.join()
