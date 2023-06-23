import asyncio
import json
import random
import string
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Generator

import httpx
from bs4 import BeautifulSoup

from app.utils import retries, Retrying


@dataclass(repr=False)
class Video:
    url: str = ""
    description: str = ""
    content: Optional[bytes] = None

    @property
    def is_empty(self) -> bool:
        return not self.content

    @property
    def caption(self) -> str:
        return f"{self.description}\n\n{self.url}"


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


class TikTokAPI:
    @classmethod
    async def download_videos(cls, urls: list[str]) -> Generator[Video, None, None]:
        tasks = [cls.download_video(url) for url in urls]
        for task in asyncio.as_completed(tasks):
            video = await task
            yield video

    @classmethod
    @retries(times=3)
    async def download_video(cls, url: str) -> Video:
        async with AsyncTikTokClient() as client:
            page = await client.get(url)
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
                    raise Retrying("video_id is different from page_id")
                description = data["desc"]
                link = data["video"]["downloadAddr"].encode("utf-8").decode("unicode_escape")
                if video := await client.get(link):
                    video.raise_for_status()
                    return Video(url=url, description=description, content=video.content)
            return Video(url=url, description="", content=None)
