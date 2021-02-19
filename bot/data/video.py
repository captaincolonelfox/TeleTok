from attr import attrs, attrib
from typing import Optional


@attrs(slots=True, auto_attribs=True, order=False, eq=False)
class VideoData:
    url: Optional[str] = attrib(default=None)
    content: Optional[bytes] = attrib(default=None)
