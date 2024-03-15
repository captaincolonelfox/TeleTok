import asyncio

from aiogram import Bot

from bot import dp, get_message
from settings import API_TOKEN


async def start() -> None:
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
