import json
from typing import Any, Optional

from bot.api import API


class TikTokAPI(API):

    @property
    def headers(self) -> dict[str, Any]:
        return {
            "Referer": "https://www.tiktok.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        }

    @property
    def links(self):
        return ['tiktok.com']

    @property
    def regexp_key(self) -> str:
        return r'"downloadAddr":"'

    def _parse_data(self, script: str) -> Optional[str]:
        js = json.loads(script)
        return js.get('props', {})\
                 .get('pageProps', {})\
                 .get('itemInfo', {})\
                 .get('itemStruct', {})\
                 .get('video', {})\
                 .get('downloadAddr')
