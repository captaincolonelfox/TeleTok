from aiogram import Bot, Dispatcher
from bot.api.likee import LikeeAPI
from bot.api.tiktok import TikTokAPI
from settings import API_TOKEN


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)


from . import handlers
