from __future__ import annotations

from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SectionDefinition(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: Optional[str] = None
    subsections: List["SectionDefinition"] = Field(default_factory=list)

    model_config = {"extra": "forbid", "arbitrary_types_allowed": False}


SectionDefinition.update_forward_refs()
