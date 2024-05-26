import asyncio

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession

from bot import dp
from settings import settings


async def start() -> None:
    session = AiohttpSession(proxy=settings.proxy)
    bot = Bot(token=settings.api_token, session=session)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
