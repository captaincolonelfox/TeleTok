import json
import os
from dataclasses import dataclass


@dataclass
class Settings:
    api_token: str
    allowed_ids: list[int]
    reply_to_message: bool
    with_captions: bool


def parse_env_list(key: str) -> list[int]:
    return json.loads(os.getenv(key, "[]"))


def parse_env_bool(key: str) -> bool:
    return os.getenv(key, "false").lower() in ("yes", "true", "1", "on")


settings = Settings(
    api_token=os.getenv("API_TOKEN", ""),
    allowed_ids=parse_env_list("ALLOWED_IDS"),
    reply_to_message=parse_env_bool("REPLY_TO_MESSAGE"),
    with_captions=parse_env_bool("WITH_CAPTIONS"),
)
