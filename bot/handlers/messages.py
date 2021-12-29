from aiogram.types import Message
from bot import dp, bot
from bot.api import MobileTikTokAPI, TikTokAPI


platforms = [MobileTikTokAPI(), TikTokAPI()]


@dp.message_handler()
async def get_message(message: Message):
    for api in platforms:
        if videos := await api.handle_message(message):
            for video in videos:
                await bot.send_video(message.chat.id, video, reply_to_message_id=message.message_id)
            break
