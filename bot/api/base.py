import asyncio
import re
from abc import ABC, abstractmethod
from typing import Any, List
import httpx
import sentry_sdk
from aiogram.types import Message
from httpx import HTTPStatusError
from bot.data import VideoData


def retries(times: int):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return await func(*args, **kwargs)
                except Exception:
                    await asyncio.sleep(0.5)
        return wrapper
    return decorator


class API(ABC):

    @property
    def headers(self) -> dict[str, Any]:
        return {
            "Referer": "https://www.tiktok.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        }

    @property
    def cookies(self) -> dict[str, Any]:
        return {
            'tt_webid_v2': '1234567890123456789'
        }

    @property
    @abstractmethod
    def links(self) -> List[str]:
        return ['platform.com']

    @property
    @abstractmethod
    def regexp_key(self) -> str:
        return 'key'

    async def handle_message(self, message: Message) -> List[VideoData]:
        urls = []
        for e in message.entities:
            for link in self.links:
                if link in (url := message.text[e.offset:e.offset + e.length]):
                    urls.append(url if url.startswith('http') else f'https://{url}')
        try:
            return [await self.download_video(url) for url in urls]
        except (KeyError, HTTPStatusError) as ex:
            sentry_sdk.capture_exception(ex)
        return []

    @retries(times=2)
    async def download_video(self, url: str) -> VideoData:
        async with httpx.AsyncClient(headers=self.headers, timeout=30,
                                     cookies=self.cookies, follow_redirects=True) as client:
            page = await client.get(url)
            for link in re.findall(self.regexp_key, page.text):
                link = link.encode('utf-8').decode('unicode_escape')
                if video := await client.get(link):
                    video.raise_for_status()
                    return VideoData(link, video.content)
        return VideoData()
