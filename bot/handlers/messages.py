from aiogram.dispatcher.filters import IDFilter
from aiogram.types import Message
from bot import bot, dp
from bot.api import TikTokAPI
from settings import USER_ID


TikTok = TikTokAPI(
    link='tiktok.com',
    regexp_key=r'"video":{"id":"(.*?)",.*?"downloadAddr":"(.*?)",.*?}',
    headers={
        "Referer": "https://www.tiktok.com/",
    }
)


def filter_message_handler(user_id: str):
    if user_id:
        return dp.message_handler(IDFilter(user_id=user_id))
    else:
        return dp.message_handler()


@filter_message_handler(USER_ID)
async def get_message(message: Message):
    async for video in TikTok.handle_message(message):
        if not video: continue
        await bot.send_video(message.chat.id, video, reply_to_message_id=message.message_id)
