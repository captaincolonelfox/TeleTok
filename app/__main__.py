from aiogram.utils import executor

from app.bot import dp

if __name__ == "__main__":
    executor.start_polling(dp)
