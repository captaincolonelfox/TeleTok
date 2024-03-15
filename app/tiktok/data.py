from dataclasses import dataclass, field
from typing import Optional, Generator


@dataclass
class Tiktok:
    url: str = ""
    description: str = ""

    @property
    def is_empty(self) -> bool:
        raise NotImplementedError

    @property
    def caption(self) -> str:
        return f"{self.description}\n\n{self.url}"


@dataclass
class EmptyTiktok(Tiktok):
    @property
    def is_empty(self) -> bool:
        return True


@dataclass(repr=False)
class Video(Tiktok):
    video: Optional[bytes] = None

    @property
    def is_empty(self) -> bool:
        return not self.video


@dataclass
class Photo(Tiktok):
    photos: list[str] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not self.photos

    def get_chunks(self, size: int) -> Generator[str, None, None]:
        for n in range(0, len(self.photos), size):
            yield self.photos[n : n + size]


@dataclass
class ItemStruct:
    page_id: str
    video_url: str
    photo_urls: list[str]
    description: str

    @classmethod
    def parse(cls, data: dict) -> "ItemStruct":
        return ItemStruct(
            page_id=data["id"],
            video_url=(
                (data["video"].get("playAddr", "") or data["video"].get("downloadAddr"))
                .encode()
                .decode("unicode_escape")
            ),
            photo_urls=[
                photo["imageURL"]["urlList"][0]
                for photo in data.get("imagePost", {}).get("images", [])
            ],
            description=data["desc"],
        )
