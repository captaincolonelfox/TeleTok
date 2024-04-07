from aiogram import Bot, Dispatcher, F
from aiogram.types import BufferedInputFile, Message

from settings import settings
from tiktok.api import TikTokAPI

dp = Dispatcher()

filters = [
    F.text.contains("tiktok.com"),
    (not settings.allowed_ids)
    | F.chat.id.in_(settings.allowed_ids)
    | F.from_user.id.in_(settings.allowed_ids),
]


@dp.message(*filters)
@dp.channel_post(*filters)
async def handle_tiktok_request(message: Message, bot: Bot) -> None:
    entries = [
        message.text[e.offset : e.offset + e.length]
        for e in message.entities or []
        if message.text is not None
    ]

    urls = [
        u if u.startswith("http") else f"https://{u}"
        for u in filter(lambda e: "tiktok.com" in e, entries)
    ]

    async for tiktok in TikTokAPI.download_tiktoks(urls):
        if not tiktok.video:
            continue

        video = BufferedInputFile(tiktok.video, filename="video.mp4")
        caption = tiktok.caption if settings.with_captions else None

        if settings.reply_to_message:
            await message.reply_video(video=video, caption=caption)
        else:
            await bot.send_video(chat_id=message.chat.id, video=video, caption=caption)
