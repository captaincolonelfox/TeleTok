import asyncio
import logging

import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from bot import bot, dp, handlers
from bot.handlers.messages import platforms
from settings import ENVIRONMENT, SENTRY_DSN

sentry_sdk.init(
    SENTRY_DSN,
    environment=ENVIRONMENT,
    integrations=[AioHttpIntegration()]
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