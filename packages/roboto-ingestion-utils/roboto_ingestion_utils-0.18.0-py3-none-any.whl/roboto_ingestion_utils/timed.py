import functools
import logging
import logging.handlers
import time
import typing

T = typing.TypeVar("T")
P = typing.ParamSpec("P")
Decorator = typing.Callable[[typing.Callable[P, T]], typing.Callable[P, T]]


class Timed:
    def __init__(self, logger_name: str):
        self.logger_name = logger_name

    def __call__(self) -> Decorator:
        def decorator(func: typing.Callable[P, T]) -> typing.Callable[P, T]:
            func_name = f"{func.__module__}.{func.__name__}"

            @functools.wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                logger = logging.getLogger(self.logger_name)
                start_time = time.perf_counter()
                ret = func(*args, **kwargs)
                elapsed_s = time.perf_counter() - start_time
                elapsed_ms = elapsed_s * 1000
                logger.debug(f"{func_name},{elapsed_ms},ms")
                return ret

            return wrapper

        return decorator
