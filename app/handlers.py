from aiogram.types import Message, MediaGroup, InputMediaPhoto

from tiktok import TikTokAPI, Video, Photo
from bot import telegram_message_handler
from settings import USER_ID


@telegram_message_handler(USER_ID)
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
            await message.reply_video(tiktok.video, caption=tiktok.caption)
        if isinstance(tiktok, Photo):
            for photos in tiktok.get_chunks(size=10):
                first_with_caption = [
                    InputMediaPhoto(photos[0], caption=tiktok.caption)
                ]
                others_without_caption = [
                    InputMediaPhoto(photo) for photo in photos[1:]
                ]
                media = MediaGroup(medias=first_with_caption + others_without_caption)
                await message.reply_media_group(media)
