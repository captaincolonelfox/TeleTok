from aiogram import Dispatcher, F
from aiogram.types import BufferedInputFile, Message

from settings import ALLOWED_IDS
from tiktok.api import TikTokAPI

dp = Dispatcher()

filters = [
    F.text.contains("tiktok.com"),
    (not ALLOWED_IDS)
    | F.chat.id.in_(ALLOWED_IDS)
    | F.from_user.id.in_(ALLOWED_IDS)
]


@dp.message(*filters)
@dp.channel_post(*filters)
async def handle_tiktok_request(message: Message) -> None:
    entries = [
        message.text[e.offset: e.offset + e.length]
        for e in message.entities or []
        if message.text is not None
    ]
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
