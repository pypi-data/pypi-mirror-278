from threading import Thread
from time import sleep

import pytest

from mtb.core.thread import Signal, ThreadManager


def test_signal():
    s = Signal()
    results = []

    def callback(value):
        results.append(value)

    s.connect(callback)
    s.emit(42)
    assert results == [42]

    s.disconnect(callback)
    s.emit(100)
    assert results == [42]  # Should not change because callback is disconnected


def test_thread_manager():
    tm = ThreadManager()
    results = []

    def slow_function():
        sleep(0.1)
        results.append("finished")

    def on_start():
        results.append("started")

    def on_finish():
        results.append("all_finished")

    thread = Thread(target=slow_function)

    tm.add_thread(thread)
    tm.started_signal.connect(on_start)
    tm.finished_signal.connect(on_finish)

    tm.start_all_threads()
    assert "started" in results

    tm.join_all_threads()
    assert "all_finished" in results
    assert "finished" in results
