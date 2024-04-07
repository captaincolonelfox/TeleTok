import asyncio
import logging
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import ParamSpec, TypeVar


class RetryingError(Exception):
    pass


class NoScriptError(RetryingError):
    def __init__(self) -> None:
        super().__init__("no script")


class NoDataError(RetryingError):
    def __init__(self) -> None:
        super().__init__("no data")


class DifferentPageError(RetryingError):
    def __init__(self) -> None:
        super().__init__("tiktok_id is different from page_id")


P = ParamSpec("P")
T = TypeVar("T")

Wrapper = Callable[P, Awaitable[T | None]]
Decorator = Callable[[Callable[P, Awaitable[T]]], Wrapper]


def retries(times: int) -> Decorator:
    def decorator(func: Callable[P, Awaitable[T]]) -> Wrapper:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | None:
            for _ in range(times):
                try:
                    return await func(*args, **kwargs)
                except RetryingError:
                    logging.exception("Retrying")
                    await asyncio.sleep(0.5)
            return None

        return wrapper

    return decorator
