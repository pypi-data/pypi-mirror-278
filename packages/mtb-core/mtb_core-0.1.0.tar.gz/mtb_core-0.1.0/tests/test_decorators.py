import asyncio

import pytest

from mtb.core.decorators import (
    batch_processing,
    collect_metrics,
    deprecated,
    emit_events,
    format_output,
    handle_errors,
    resource_cleanup,
    retry,
    timeout,
    transform_args,
    validate_input,
)


# Mock classes and functions for testing
class FakeResource:
    def __init__(self):
        self.cleaned_up = False

    def cleanup(self):
        self.cleaned_up = True


class FakeCollector:
    def __init__(self):
        self.data = []

    def record(self, metric):
        self.data.append(metric)


class FakeEmitter:
    def __init__(self):
        self.emitted = False

    def emit(self):
        self.emitted = True


# 1. Error Handling
def test_handle_errors():
    @handle_errors(fallback_func=lambda: "fallback")
    def faulty_func():
        raise ValueError("An exception")

    assert faulty_func() == "fallback"


def test_handle_errors2():
    @handle_errors(fallback_func=lambda: "fallback")
    def faulty_func():
        raise ValueError("An exception")

    assert faulty_func() == "fallback"


# 7. Resource Cleanup
def test_resource_cleanup():
    resource = FakeResource()

    @resource_cleanup(resource)
    def some_func():
        pass

    some_func()
    assert resource.cleaned_up


# 8. Retry Mechanism
def test_retry():
    counter = 0

    @retry(attempts=3)
    def unreliable_func():
        nonlocal counter
        counter += 1
        raise ValueError("An exception")

    with pytest.raises(ValueError):
        unreliable_func()
    assert counter == 3


# 10. Input Validation
def test_validate_input():
    @validate_input(int)
    def func(x):
        return x * 2

    with pytest.raises(TypeError):
        func("string")

    assert func(10) == 20


# 11. Output Formatting
def test_format_output():
    @format_output("{:.2f}")
    def func():
        return 3.14159

    assert func() == "3.14"


# 12. Telemetry/Metrics Collection
def test_collect_metrics():
    collector = FakeCollector()

    @collect_metrics(collector)
    def func():
        pass

    func()
    assert len(collector.data) == 1


# 13. Timeout
@pytest.mark.asyncio
async def test_timeout():
    @timeout(1)
    async def slow_func():
        await asyncio.sleep(0.5)

    await slow_func()


# 14. Deprecation Warning
def test_deprecated(caplog):
    @deprecated
    def old_func():
        pass

    old_func()
    assert "is deprecated" in caplog.text


# 16. Event Emitting
def test_emit_events():
    start_emitter = FakeEmitter()
    end_emitter = FakeEmitter()

    @emit_events(start_emitter, end_emitter)
    def func():
        pass

    func()
    assert start_emitter.emitted
    assert end_emitter.emitted


# 17. Argument Transformation
def test_transform_args():
    @transform_args(lambda args: (x * 2 for x in args))
    def func(a, b):
        return a + b

    assert func(2, 3) == 10


# 19. Batching
def test_batch_processing():
    data = list(range(10))

    @batch_processing(3)
    def process_batch(batch):
        for item in batch:
            assert item < 10

    process_batch(data)
