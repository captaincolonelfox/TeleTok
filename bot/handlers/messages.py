from aiogram.types import Message
from bot import dp, bot
from bot.api import TikTokAPI


TikTok = TikTokAPI(
    link='tiktok.com',
    regexp_key=r'"downloadAddr":"(.*?)",',
    headers={
        "Referer": "https://www.tiktok.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    }, cookies={'tt_webid_v2': '1234567890123456789'},
)


@dp.message_handler()
async def get_message(message: Message):
    async for video in TikTok.handle_message(message):
        if not video: continue
        await bot.send_video(message.chat.id, video, reply_to_message_id=message.message_id)
