import json
from typing import Optional, List

from bot.api import API


class TikTokAPI(API):

    @property
    def links(self) -> List[str]:
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
