from __future__ import annotations

from pydantic import BaseModel
from typing import Optional

from .settings import WalkthroughSettings


class WalkthroughConfig(BaseModel):
    settings: WalkthroughSettings
    enabled: bool = True
    default_persona: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}
