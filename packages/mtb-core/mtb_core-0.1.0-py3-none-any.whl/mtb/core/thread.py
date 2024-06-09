import weakref


class Signal:
    """Very basic signal"""

    def __init__(self):
        self._callbacks = weakref.WeakValueDictionary()

    def connect(self, callback):
        self._callbacks[callback] = callback

    def disconnect(self, callback):
        self._callbacks.pop(callback, None)

    def emit(self, *args, **kwargs):
        callbacks = self._callbacks.copy()
        for callback in callbacks:
            callback(*args, **kwargs)


class ThreadManager(object):
    started_signal = Signal()
    finished_signal = Signal()

    def __init__(self):
        self.threads = []

    def add_thread(self, thread):
        self.threads.append(thread)

    def start_all_threads(self):
        for thread in self.threads:
            thread.start()
        self.started_signal.emit()

    def join_all_threads(self):
        for thread in self.threads:
            thread.join()
        self.finished_signal.emit()
