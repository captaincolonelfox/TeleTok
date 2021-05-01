import json
from typing import Any, Optional

from bot.api import API


class LikeeAPI(API):

    @property
    def headers(self) -> dict[str, Any]:
        return {
            "Referer": "https://www.likee.video/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        }

    @property
    def links(self):
        return ['likee.video', 'like-video.com']

    @property
    def regexp_key(self) -> str:
        return r'"video_url":'

    def _parse_data(self, script: str) -> Optional[str]:
        js = json.loads(script.split('window.data = ')[-1][:-1])
        return js.get('video_url')
