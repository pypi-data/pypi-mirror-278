import asyncio, logging, time
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Tuple, Type, Union

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_errors(fallback_func: Callable[..., Any] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                if fallback_func:
                    return fallback_func(*args, **kwargs)

        return wrapper

    return decorator


def timer(name):
    def timer_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            startTime = datetime.now()
            logger.info(f'starttime: {startTime.strftime("%Y-%m-%d %H:%M:%S")}')
            func(*args, **kwargs)
            endTime = datetime.now()
            logger.info(f'endtime: {endTime.strftime("%Y-%m-%d %H:%M:%S")}')
            logger.info(f"duration: {endTime - startTime}")

        return func_wrapper

    return timer_decorator


def resource_cleanup(resource):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            finally:
                resource.cleanup()

        return wrapper

    return decorator


def retry(attempts: int, delay: int = 1):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt failed: {e}, retrying...")
                    time.sleep(delay)
            if last_exception:
                raise last_exception

        return wrapper

    return decorator


def validate_input(param_type: Type[Any]):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not all(isinstance(arg, param_type) for arg in args):
                raise TypeError("Invalid input type")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def format_output(format_spec: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return format_spec.format(result)

        return wrapper

    return decorator


def collect_metrics(metric_collector):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            metric_collector.record(end_time - start_time)
            return result

        return wrapper

    return decorator


def timeout(seconds):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            future = asyncio.ensure_future(func(*args, **kwargs))
            try:
                return await asyncio.wait_for(future, timeout=seconds)
            except asyncio.TimeoutError:
                future.cancel()
                raise asyncio.TimeoutError(f"{func.__name__} timed out after {seconds} seconds")

        return wrapper

    return decorator


def deprecated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.warning(f"{func.__name__} is deprecated.")
        return func(*args, **kwargs)

    return wrapper


def emit_events(on_start, on_end):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            on_start.emit()
            result = func(*args, **kwargs)
            on_end.emit()
            return result

        return wrapper

    return decorator


def transform_args(transform_func: Callable[[Tuple], Tuple]):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            transformed_args = transform_func(args)
            return func(*transformed_args, **kwargs)

        return wrapper

    return decorator


def batch_processing(batch_size: int):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(iterable, *args, **kwargs):
            for i in range(0, len(iterable), batch_size):
                func(iterable[i : i + batch_size], *args, **kwargs)

        return wrapper

    return decorator
