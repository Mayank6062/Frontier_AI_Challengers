from __future__ import annotations

from typing import Dict, Optional, Protocol
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class SectionRenderContract(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    type: str
    source_field: str
    template_id: Optional[str] = None
    persona_visibility: Optional[Dict[str, str]] = None
    print_behavior: Optional[str] = None
    anchor: Optional[str] = None
    parent_section: Optional[UUID] = None
    order: int = 0

    model_config = {"extra": "forbid", "frozen": True}


class SectionTemplateMetadata(BaseModel):
    template_id: str
    version: str
    engine: Optional[str] = None
    metadata: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid", "frozen": True}


class SectionRenderer(Protocol):
    def render_section(self, section: SectionRenderContract) -> str:
        """Render a section into HTML fragment (contract only)."""


class SectionTemplateResolver(Protocol):
    def resolve(
        self, template_id: str, version: Optional[str] = None
    ) -> SectionTemplateMetadata:
        """Resolve template metadata by id and optional version."""
