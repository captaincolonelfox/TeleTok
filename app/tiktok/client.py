import json
import random
import string
from datetime import UTC, datetime

import httpx
from bs4 import BeautifulSoup

from tiktok.data import ItemStruct
from utils import DifferentPageError, NoDataError, NoScriptError, retries


class AsyncTikTokClient(httpx.AsyncClient):
    def __init__(self) -> None:
        super().__init__(
            headers={
                "Referer": "https://www.tiktok.com/",
                "User-Agent": (
                    f"{''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 10)))}-"
                    f"{''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 7)))}/"
                    f"{random.randint(10, 300)} "
                    f"({datetime.now(tz=UTC).replace(microsecond=0).timestamp()})"
                ),
            },
            timeout=30,
            cookies={
                "tt_webid_v2": f"{random.randint(10 ** 18, (10 ** 19) - 1)}",
            },
            follow_redirects=True,
        )

    @retries(times=3)
    async def get_page_data(self, url: str) -> ItemStruct:
        page = await self.get(url)
        page_id = page.url.path.rsplit("/", 1)[-1]

        soup = BeautifulSoup(page.text, "html.parser")

        if script := soup.select_one('script[id="__UNIVERSAL_DATA_FOR_REHYDRATION__"]'):
            script = json.loads(script.text)
        else:
            raise NoScriptError

        try:
            data = script["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]
        except KeyError as ex:
            raise NoDataError from ex

        if data["id"] != page_id:
            raise DifferentPageError
        return ItemStruct.parse(data)

    async def get_video(self, url: str) -> bytes | None:
        resp = await self.get(url)
        if resp.is_error:
            return None
        return resp.content
