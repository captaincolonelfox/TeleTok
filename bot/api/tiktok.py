import json
from typing import Any

from bot.api import API


class TikTokAPI(API):

    @property
    def headers(self) -> dict[str, Any]:
        return {'Referer': 'https://www.tiktok.com/'}

    @property
    def links(self):
        return ['tiktok.com']

    @property
    def regexp_key(self) -> str:
        return r'"downloadAddr":"'

    def _parse_data(self, script: str) -> str:
        js = json.loads(script)
        return js['props']['pageProps']['itemInfo']['itemStruct']['video']['downloadAddr']