import json
import os
from typing import List

def _parse_env(key: str, default):
    return json.loads(value) if (value := os.getenv(key)) else default

API_TOKEN: str = os.getenv("API_TOKEN")
ALLOWED_IDS: List[int] = _parse_env('ALLOWED_IDS', [])
REPLY_TO_MESSAGE: bool = _parse_env('REPLY_TO_MESSAGE', True)
WITH_CAPTIONS: bool = _parse_env('WITH_CAPTIONS', True)
