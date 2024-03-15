from aiogram import Dispatcher, F
from aiogram.types import Message, BufferedInputFile, InputMediaPhoto

from settings import USER_ID
from tiktok.api import TikTokAPI
from tiktok.data import Video, Photo

dp = Dispatcher()
filters = [
    F.text.contains("tiktok.com"),
    (USER_ID is None) | (F.from_user.id == USER_ID),
]


@dp.message(*filters)
@dp.channel_post(*filters)
async def get_message(message: Message):
    entries = [message.text[e.offset : e.offset + e.length] for e in message.entities]
    urls = [
        u if u.startswith("http") else f"https://{u}"
        for u in filter(lambda e: "tiktok.com" in e, entries)
    ]
    async for tiktok in TikTokAPI.download_tiktoks(urls):
        if tiktok.is_empty:
            continue
        if isinstance(tiktok, Video):
            await message.reply_video(
                video=BufferedInputFile(tiktok.video, filename="video.mp4"),
                caption=tiktok.caption,
            )
        if isinstance(tiktok, Photo):
            for photos in tiktok.get_chunks(size=10):
                first_with_caption = [InputMediaPhoto(media=photos[0], caption=tiktok.caption)]
                others_without_caption = [InputMediaPhoto(media=photo) for photo in photos[1:]]
                await message.reply_media_group(first_with_caption + others_without_caption)
