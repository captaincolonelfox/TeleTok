import asyncio
import logging
from functools import wraps


class RetryingError(Exception):
    pass


def retries(times: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return await func(*args, **kwargs)
                except RetryingError:
                    logging.exception("Retrying")
                    await asyncio.sleep(0.5)

        return wrapper

    return decorator
