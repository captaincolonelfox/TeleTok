import re
from abc import ABC, abstractmethod
from typing import Any, List, Optional

import httpx
import sentry_sdk
from aiogram.types import Message
from bs4 import BeautifulSoup
from httpx import HTTPStatusError


class API(ABC):
    client = httpx.AsyncClient(
        headers={
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
    )

    @property
    def headers(self) -> dict[str, Any]:
        return {'Referer': 'https://www.platform.com/'}

    @property
    @abstractmethod
    def links(self) -> List[str]:
        return ['platform.com']

    @property
    @abstractmethod
    def regexp_key(self) -> str:
        return 'key'

    async def handle_message(self, message: Message) -> List[bytes]:
        urls = []
        for e in message.entities:
            for link in self.links:
                if link in (url := message.text[e.offset:e.offset + e.length]):
                    urls.append(url)
        if not urls:
            return []
        try:
            return [await self.download_video(url) for url in urls]
        except (KeyError, HTTPStatusError) as ex:
            sentry_sdk.capture_exception(ex)
            return []

    async def download_video(self, url: str) -> Optional[bytes]:
        page = await self.client.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        if data := soup(text=re.compile(self.regexp_key)):
            for script in data:
                if link := self._parse_data(script):
                    video = await self.client.get(link, headers=self.headers)
                    video.raise_for_status()
                    return video.content
                return None

    @abstractmethod
    def _parse_data(self, script: str) -> str:
        pass
