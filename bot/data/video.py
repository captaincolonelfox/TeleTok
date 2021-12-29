from attr import define, field
from typing import Optional


@define
class VideoData:
    url: Optional[str] = field(default=None)
    content: Optional[bytes] = field(default=None)
