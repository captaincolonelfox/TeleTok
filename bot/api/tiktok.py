import asyncio
import json
import logging
import random
import string
from datetime import datetime
from functools import wraps
from typing import AsyncIterator
import httpx
from aiogram.types import Message
from attr import define, field
from settings import USER_AGENT
from bs4 import BeautifulSoup


class Retrying(Exception):
    pass


def retries(times: int):
    def decorator(func):
        @wraps(func)
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
    link: str = field(default='tiktok.com', converter=str)
    script_selector: str = field(default='script[id="SIGI_STATE"]', converter=str)

    async def handle_message(self, message: Message) -> AsyncIterator[tuple[str, str, bytes]]:
        entries = (message.text[e.offset:e.offset + e.length] for e in message.entities)
        urls = map(
            lambda u: u if u.startswith('http') else f'https://{u}',
            filter(lambda e: self.link in e, entries)
        )
        for url in urls:
            description, video = await self.download_video(url)
            yield url, description, video

    @retries(times=3)
    async def download_video(self, url: str) -> tuple[str, bytes]:
        async with httpx.AsyncClient(headers=self.headers, timeout=30,
                                     cookies=self._tt_webid_v2, follow_redirects=True) as client:
            page = await client.get(url, headers=self._user_agent)
            page_id = page.url.path.rsplit('/', 1)[-1]

            soup = BeautifulSoup(page.text, 'html.parser')

            if script := soup.select_one(self.script_selector):
                script = json.loads(script.text)
            else:
                raise Retrying("no script")

            modules = tuple(script.get("ItemModule").values())
            if not modules:
                raise Retrying("no modules")

            for data in modules:
                if data["id"] != page_id:
                    raise Retrying("video_id is different from page_id")
                description = data["desc"]
                link = data["video"]["downloadAddr"].encode('utf-8').decode('unicode_escape')
                if video := await client.get(link, headers=self._user_agent):
                    video.raise_for_status()
                    return description, video.content

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

    @property
    def _tt_webid_v2(self):
        return {'tt_webid_v2': f"{random.randint(10 ** 18, (10 ** 19) - 1)}"}
