from dataclasses import dataclass


@dataclass
class Tiktok:
    url: str = ""
    description: str = ""
    video: bytes | None = None

    @property
    def caption(self) -> str:
        return f"{self.description}\n\n{self.url}"


@dataclass
class ItemStruct:
    page_id: str
    video_url: str
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
            description=data["desc"],
        )
