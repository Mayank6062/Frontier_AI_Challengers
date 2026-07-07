from __future__ import annotations

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class WalkthroughManifestEntry(BaseModel):
    id: UUID
    title: str
    created_at: datetime

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughManifest(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    version: str
    entries: list[WalkthroughManifestEntry]

    model_config = {"extra": "forbid", "frozen": True}
