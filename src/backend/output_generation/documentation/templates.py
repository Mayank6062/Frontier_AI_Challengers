from __future__ import annotations

from typing import Sequence, Optional
from pydantic import BaseModel, Field


class TemplateVariable(BaseModel):
    name: str
    description: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class TemplateDefinition(BaseModel):
    template_id: str
    version: str
    path: Optional[str]
    placeholders: Sequence[TemplateVariable] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class TemplateManifest(BaseModel):
    templates: Sequence[TemplateDefinition]

    model_config = {"extra": "forbid", "frozen": True}
