import asyncio
import logging
import random
import re
import string
from datetime import datetime
from typing import AsyncIterator, Optional
import httpx
from aiogram.types import Message
from attr import define, field
from settings import USER_AGENT


def retries(times: int):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return await func(*args, **kwargs)
                except Exception as ex:
                    logging.exception(ex)
                    await asyncio.sleep(0.5)
        return wrapper
    return decorator


@define
class TikTokAPI:
    headers: dict = field(converter=dict)
    cookies: dict = field(converter=dict)
    link: str = field(converter=str)
    regexp_key: str = field(converter=str)

    async def handle_message(self, message: Message) -> AsyncIterator[Optional[bytes]]:
        entries = (message.text[e.offset:e.offset + e.length] for e in message.entities)
        urls = map(
            lambda u: u if u.startswith('http') else f'https://{u}',
            filter(lambda e: self.link in e, entries)
        )
        for url in urls:
            video = await self.download_video(url)
            yield video

    @retries(times=3)
    async def download_video(self, url: str) -> Optional[bytes]:
        async with httpx.AsyncClient(headers=self.headers, timeout=30,
                                     cookies=self.cookies, follow_redirects=True) as client:
            page = await client.get(url, headers=self._user_agent)
            tid = page.url.path.rsplit('/', 1)[-1]
            for vid, link in re.findall(self.regexp_key, page.text):
                if vid != tid: raise Exception("Retrying")
                link = link.encode('utf-8').decode('unicode_escape')
                if video := await client.get(link, headers=self._user_agent):
                    video.raise_for_status()
                    return video.content

    @property
    def _user_agent(self) -> dict:
        return {
            'User-Agent': USER_AGENT or (
                f"{''.join(random.choices(string.ascii_lowercase, k=random.randint(4,10)))}-"
                f"{''.join(random.choices(string.ascii_lowercase, k=random.randint(3,7)))}/"
                f"{random.randint(10, 300)} "
                f"({datetime.now().replace(microsecond=0).timestamp()})"
            )
        }
