import asyncio
import logging

import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from bot import bot, dp, handlers  # noqa
from settings import ENVIRONMENT, SENTRY_DSN

sentry_sdk.init(
    dsn=SENTRY_DSN,
    environment=ENVIRONMENT,
    integrations=[
        AioHttpIntegration(),
        LoggingIntegration()
    ]
)


async def main():
    try:
        logging.info('Started')
        await dp.start_polling()
    finally:
        logging.info('Exited')
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())