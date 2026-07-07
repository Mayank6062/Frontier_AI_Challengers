from __future__ import annotations

from typing import NamedTuple, Optional, Sequence
from uuid import UUID

from pydantic import BaseModel

from .models import WalkthroughReference


class WalkthroughRegistryEntry(NamedTuple):
    id: UUID
    title: str
    manifest_ref: Optional[str]


class WalkthroughRegistryIndex(BaseModel):
    entries: Sequence[WalkthroughReference]

    model_config = {"extra": "forbid", "frozen": True}
