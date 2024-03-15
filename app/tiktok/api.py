import asyncio
from typing import Generator

from tiktok.client import AsyncTikTokClient
from tiktok.data import Tiktok, EmptyTiktok, Video, Photo


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
            if item := await client.get_page_data(url=url):
                if item.video_url:
                    video = await client.get_video(url=item.video_url)
                    return Video(url=url, description=item.description, video=video)
                if item.photo_urls:
                    return Photo(url=url, description=item.description, photos=item.photo_urls)
            return EmptyTiktok()
