import asyncio

from aiogram import Bot

from settings import settings
from bot import dp


async def start() -> None:
    bot = Bot(token=settings.api_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
