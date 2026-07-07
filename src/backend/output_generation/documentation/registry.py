from __future__ import annotations

from typing import Sequence

from pydantic import BaseModel


class DocumentRegistryEntry(BaseModel):
    name: str
    description: str
    document_type: str

    model_config = {"extra": "forbid", "frozen": True}


class DocumentRegistryManifest(BaseModel):
    entries: Sequence[DocumentRegistryEntry]

    model_config = {"extra": "forbid", "frozen": True}
