from typing import List
from bot.api import API


class TikTokAPI(API):

    @property
    def links(self) -> List[str]:
        return ['tiktok.com']

    @property
    def regexp_key(self) -> str:
        return r'downloadAddr":"(.*?)",'


class MobileTikTokAPI(API):

    @property
    def links(self) -> List[str]:
        return ['vm.tiktok.com']

    @property
    def regexp_key(self) -> str:
        return r'urls":\["(.*?)"\]'
