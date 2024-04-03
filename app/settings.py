import json
import os
from typing import List

API_TOKEN: str = os.getenv("API_TOKEN")
ALLOWED_IDS: List[int] = json.loads(allowed_ids_raw) if (
    allowed_ids_raw := os.getenv("ALLOWED_IDS")
) else []
