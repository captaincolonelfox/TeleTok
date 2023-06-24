from aiogram.utils import executor
from bot import dp
from handlers import get_message  # noqa

if __name__ == "__main__":
    executor.start_polling(dp)
