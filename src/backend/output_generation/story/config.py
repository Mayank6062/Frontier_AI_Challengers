from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class StoryConfig(BaseModel):
    enabled: bool = True
    default_depth: Optional[str] = None
    default_tone: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}
