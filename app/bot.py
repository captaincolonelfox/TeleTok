from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters import IDFilter
from settings import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)


def telegram_message_handler(user_id: str = None):
    filters = []
    if user_id:
        filters.append(IDFilter(user_id=user_id))

    def decorator(func):
        dp.register_channel_post_handler(func, *filters)
        dp.register_message_handler(func, *filters)
        return func

    return decorator
