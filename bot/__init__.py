from aiogram import Bot, Dispatcher
from settings import API_TOKEN


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)
