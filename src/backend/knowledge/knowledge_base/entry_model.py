from __future__ import annotations

from typing import Dict, Any
from pydantic import BaseModel, Field


class EntryModel(BaseModel):
    """Represents a knowledge base entry.

    Fields:
    - id: unique identifier
    - text: entry content
    - metadata: arbitrary key/value metadata
    """

    id: str
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        frozen = True
