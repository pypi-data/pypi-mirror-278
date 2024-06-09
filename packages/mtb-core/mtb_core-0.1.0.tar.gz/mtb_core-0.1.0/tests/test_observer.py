import asyncio, gc

import pytest

from mtb.core.observer import Observable, Observer


# region asyncio
class DummyAsyncObserver(Observer):
    def __init__(self):
        self.notified = False
        self.closed = False

    async def update(self, observable, *args, **kwargs):
        self.notified = True

    def close(self):
        self.closed = True


class TrickyObserver(Observer):
    def __init__(self):
        self.notified = False
        self.closed = False

    def update(self, observable, *args, **kwargs):
        self.notified = True
        observable.unsubscribe(self)  # Unsubscribe itself during notification

    def close(self):
        self.closed = True


class ResubscribingObserver(Observer):
    def __init__(self):
        self.notified = False
        self.closed = False

    def update(self, observable, *args, **kwargs):
        self.notified = True
        observable.unsubscribe(self)  # First, unsubscribe itself
        observable.subscribe(self)  # Then, resubscribe

    def close(self):
        self.closed = True


@pytest.mark.asyncio
async def test_async_observable_subscribe_unsubscribe():
    observer = DummyAsyncObserver()
    observable = Observable()
    observable.subscribe(observer)

    await observable.notify_async()

    await asyncio.sleep(0.1)  # Simulate some async operation

    # Check if the observer has been added and notified
    assert any(ref().notified == True for ref in observable._observers)

    observable.unsubscribe(observer)

    await asyncio.sleep(0.1)  # Allow time for the observer to be unsubscribed

    # Check if the observer has been removed and it is closed
    assert observer.closed == True


@pytest.mark.asyncio
async def test_multiple_async_observers_notified():
    observer1 = DummyAsyncObserver()
    observer2 = DummyAsyncObserver()
    observable = Observable()

    observable.subscribe(observer1)
    observable.subscribe(observer2)

    await observable.notify_async()

    assert all(ref().notified == True for ref in observable._observers)


@pytest.mark.asyncio
async def test_unsubscribe_during_notify():
    tricky_observer = TrickyObserver()  # Assuming this observer unsubscribes itself when notified
    observable = Observable()

    observable.subscribe(tricky_observer)

    await observable.notify_async()

    assert all(ref() is None or ref().notified == True for ref in observable._observers)


@pytest.mark.asyncio
async def test_resubscribe_during_notify():
    observer = ResubscribingObserver()
    observable = Observable()

    observable.subscribe(observer)

    await observable.notify_async()

    assert all(ref().notified == True for ref in observable._observers)


@pytest.mark.asyncio
async def test_mixed_sync_and_async_observers_notified():
    async_observer = DummyAsyncObserver()
    sync_observer = DummyObserver()
    observable = Observable()

    observable.subscribe(async_observer)
    observable.subscribe(sync_observer)

    await observable.notify_async()

    assert all(ref().notified == True for ref in observable._observers)


# endregion
# Dummy Observer class for testing
class DummyObserver(Observer):
    def __init__(self):
        self.notified = False
        self.args = ()
        self.kwargs = {}

    def update(self, observable, *args, **kwargs):
        self.notified = True
        self.args = args
        self.kwargs = kwargs


def test_observable_subscribe_unsubscribe():
    observer = DummyObserver()
    observable = Observable()

    # Subscribe
    observable.subscribe(observer)
    assert any((ref() is not None and ref().notified == False) for ref in observable._observers)

    # Unsubscribe
    observable.unsubscribe(observer)
    assert all((ref() is None or ref().notified == True) for ref in observable._observers)


def test_multiple_observers():
    observer1 = DummyObserver()
    observer2 = DummyObserver()
    observable = Observable()

    observable.subscribe(observer1)
    observable.subscribe(observer2)

    observable.notify()

    assert any((ref() is not None and ref().notified == True) for ref in observable._observers)


def test_subscribe_same_observer_multiple_times():
    observer = DummyObserver()
    observable = Observable()

    observable.subscribe(observer)
    observable.subscribe(observer)

    assert len(observable._observers) == 1


def test_unsubscribe_non_subscribed_observer():
    observer1 = DummyObserver()
    observer2 = DummyObserver()
    observable = Observable()

    observable.subscribe(observer1)

    observable.unsubscribe(observer2)  # should not raise an error
    assert len(observable._observers) == 1


def test_garbage_collected_observer():
    observable = Observable()

    observer = DummyObserver()
    observable.subscribe(observer)

    del observer  # Manually delete the observer
    gc.collect()  # Run the garbage collector

    observable.cleanup()
    assert len(observable._observers) == 0


def test_observable_notify():
    observer1 = DummyObserver()
    observer2 = DummyObserver()

    observable = Observable()
    observable.subscribe(observer1)
    observable.subscribe(observer2)

    observable.notify("data", key="value")

    # assert observer1.notified == True
    assert observer1.args == ("data",)
    assert observer1.kwargs == {"key": "value"}

    assert observer2.notified == True
    assert observer2.args == ("data",)
    assert observer2.kwargs == {"key": "value"}


def test_observable_cleanup():
    observer = DummyObserver()
    observable = Observable()
    observable.subscribe(observer)
    observable.unsubscribe(observer)
    observable.cleanup()

    # Ensure the observer references are cleaned up
    assert len(observable._observers) == 0
