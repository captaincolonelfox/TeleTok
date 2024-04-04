import asyncio

from bot import dp, bot

async def start() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start())
