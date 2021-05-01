import json
import cytoolz
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
        return cytoolz.get_in(
            ['props', 'pageProps', 'itemInfo', 'itemStruct', 'video', 'downloadAddr'],
            json.loads(script)
        )


class MobileTikTokAPI(API):

    @property
    def links(self) -> List[str]:
        return ['vm.tiktok.com']

    @property
    def regexp_key(self) -> str:
        return r'"video":{"urls"'

    def _parse_data(self, script: str) -> Optional[str]:
        script = script.split(' = ', maxsplit=1)[-1]
        urls = cytoolz.get_in(
            ['/v/:id', 'videoData', 'itemInfos', 'video', 'urls'],
            json.loads(script),
            default=[]
        )
        for url in urls:
            return url
