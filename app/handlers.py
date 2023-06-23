from aiogram.types import Message

from app.tiktok import TikTokAPI
from app.bot import telegram_message_handler, bot
from app.settings import USER_ID


@telegram_message_handler(USER_ID)
async def get_message(message: Message):
    entries = [message.text[e.offset : e.offset + e.length] for e in message.entities]
    urls = [
        u if u.startswith("http") else f"https://{u}"
        for u in filter(lambda e: "tiktok.com" in e, entries)
    ]
    async for video in TikTokAPI.download_videos(urls):
        if video.is_empty:
            continue
        await bot.send_video(
            message.chat.id,
            video.content,
            caption=video.caption,
            reply_to_message_id=message.message_id,
        )
