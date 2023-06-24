import asyncio
import json
import random
import string
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Generator

import httpx
from bs4 import BeautifulSoup

from utils import retries, Retrying


@dataclass
class Tiktok:
    url: str = ""
    description: str = ""

    @property
    def is_empty(self) -> bool:
        raise NotImplementedError

    @property
    def caption(self) -> str:
        return f"{self.description}\n\n{self.url}"


@dataclass
class EmptyTiktok(Tiktok):
    @property
    def is_empty(self) -> bool:
        return True


@dataclass(repr=False)
class Video(Tiktok):
    video: Optional[bytes] = None

    @property
    def is_empty(self) -> bool:
        return not self.video


@dataclass
class Photo(Tiktok):
    photos: list[str] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not self.photos

    def get_chunks(self, size: int) -> Generator[str, None, None]:
        for n in range(0, len(self.photos), size):
            yield self.photos[n : n + size]


class AsyncTikTokClient(httpx.AsyncClient):
    def __init__(self):
        super().__init__(
            headers={
                "Referer": "https://www.tiktok.com/",
                "User-Agent": (
                    f"{''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 10)))}-"
                    f"{''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 7)))}/"
                    f"{random.randint(10, 300)} "
                    f"({datetime.now().replace(microsecond=0).timestamp()})"
                ),
            },
            timeout=30,
            cookies={
                "tt_webid_v2": f"{random.randint(10 ** 18, (10 ** 19) - 1)}",
            },
            follow_redirects=True,
        )

    @retries(times=3)
    async def get_page_data(self, url: str) -> dict:
        page = await self.get(url)
        page_id = page.url.path.rsplit("/", 1)[-1]

        soup = BeautifulSoup(page.text, "html.parser")

        if script := soup.select_one('script[id="SIGI_STATE"]'):
            script = json.loads(script.text)
        else:
            raise Retrying("no script")

        modules = tuple(script.get("ItemModule").values())
        if not modules:
            raise Retrying("no modules")

        for data in modules:
            if data["id"] != page_id:
                raise Retrying("tiktok_id is different from page_id")
            return data

    async def get_video(self, data: dict) -> Optional[bytes]:
        link = data["video"].get("downloadAddr", "")
        if not link:
            return None
        resp = await self.get(link.encode().decode("unicode_escape"))
        if resp.is_error:
            return None
        return resp.content

    async def get_description(self, data: dict) -> str:
        return data["desc"]

    async def get_photos(self, data: dict) -> list[str]:
        return [
            photo["imageURL"]["urlList"][0] for photo in data["imagePost"]["images"]
        ]


class TikTokAPI:
    @classmethod
    async def download_tiktoks(cls, urls: list[str]) -> Generator[Tiktok, None, None]:
        tasks = [cls.download_tiktok(url) for url in urls]
        for task in asyncio.as_completed(tasks):
            video = await task
            yield video

    @classmethod
    async def download_tiktok(cls, url: str) -> Tiktok:
        async with AsyncTikTokClient() as client:
            if data := await client.get_page_data(url=url):
                description = await client.get_description(data=data)
                if video := await client.get_video(data=data):
                    return Video(url=url, description=description, video=video)
                if photos := await client.get_photos(data=data):
                    return Photo(url=url, description=description, photos=photos)
            return EmptyTiktok()
