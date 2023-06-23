import asyncio
import logging
from functools import wraps


class Retrying(Exception):
    pass


def retries(times: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return await func(*args, **kwargs)
                except Exception as ex:
                    logging.exception(ex)
                    await asyncio.sleep(0.5)

        return wrapper

    return decorator
