import asyncio
from collections.abc import AsyncIterable

from tiktok.client import AsyncTikTokClient
from tiktok.data import Tiktok


class TikTokAPI:
    @classmethod
    async def download_tiktoks(cls, urls: list[str]) -> AsyncIterable[Tiktok]:
        tasks = [cls.download_tiktok(url) for url in urls]
        for task in asyncio.as_completed(tasks):
            tiktok = await task
            yield tiktok

    @classmethod
    async def download_tiktok(cls, url: str) -> Tiktok:
        async with AsyncTikTokClient() as client:
            if (item := await client.get_page_data(url=url)) and item.video_url:
                video = await client.get_video(url=item.video_url)
                return Tiktok(url=url, description=item.description, video=video)
            return Tiktok()
