import sentry_sdk
from aiogram.types import Message
from bot import dp, bot
from bot.api import LikeeAPI, TikTokAPI
from bot.exception import HandleException
from settings import DOWNLOAD_ERROR


platforms = [TikTokAPI(), LikeeAPI()]


@dp.message_handler()
async def get_message(message: Message):
    for api in platforms:
        for video in await api.handle_message(message):
            if video:
                if video.content:
                    await bot.send_video(
                        message.chat.id, video.content, reply_to_message_id=message.message_id
                    )
                elif video.url:
                    await bot.send_message(
                        message.chat.id, video.url, reply_to_message_id=message.message_id
                    )
            else:
                sentry_sdk.capture_exception(HandleException(message.text))
                await bot.send_message(
                    message.chat.id, DOWNLOAD_ERROR, reply_to_message_id=message.message_id
                )
