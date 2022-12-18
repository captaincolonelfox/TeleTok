from aiogram.dispatcher.filters import IDFilter
from aiogram.types import Message
from bot import bot, dp
from bot.api import TikTokAPI
from settings import USER_ID

TikTok = TikTokAPI(
    headers={
        "Referer": "https://www.tiktok.com/",
    }
)


def telegram_message_handler(user_id: str = None):
    filters = []
    if user_id:
        filters.append(IDFilter(user_id=user_id))

    def decorator(func):
        dp.register_channel_post_handler(func, *filters)
        dp.register_message_handler(func, *filters)
        return func

    return decorator


@telegram_message_handler(USER_ID)
async def get_message(message: Message):
    async for url, description, video in TikTok.handle_message(message):
        if not video:
            continue
        await bot.send_video(
            message.chat.id,
            video,
            caption=f"{description}\n\n{url}",
            reply_to_message_id=message.message_id,
        )
