from aiogram import Dispatcher, F
from aiogram.types import Message, BufferedInputFile

from settings import USER_ID
from tiktok.api import TikTokAPI

dp = Dispatcher()
filters = [
    F.text.contains("tiktok.com"),
    (USER_ID is None) | (F.from_user.id == USER_ID),
]


@dp.message(*filters)
@dp.channel_post(*filters)
async def handle_tiktok_request(message: Message):
    entries = [message.text[e.offset : e.offset + e.length] for e in message.entities]
    urls = [
        u if u.startswith("http") else f"https://{u}"
        for u in filter(lambda e: "tiktok.com" in e, entries)
    ]
    async for tiktok in TikTokAPI.download_tiktoks(urls):
        if tiktok.is_empty:
            continue
        await message.reply_video(
            video=BufferedInputFile(tiktok.video, filename="video.mp4"),
            caption=tiktok.caption,
        )
