import asyncio

from aiogram import Bot

from app import settings
from bot import dp


async def start() -> None:
    bot = Bot(token=settings.API_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
