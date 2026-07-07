from __future__ import annotations

from typing import Optional, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from .theme import VisualizationTheme
from .enums import RendererType


class VisualizationReference(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class ViewportReference(BaseModel):
    width: int
    height: int
    scale: float = 1.0

    model_config = {"extra": "forbid", "frozen": True}


class RendererReference(BaseModel):
    type: RendererType
    version: Optional[str] = None
    metadata: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid", "frozen": True}


class ThemeReference(BaseModel):
    name: str
    theme: VisualizationTheme

    model_config = {"extra": "forbid", "frozen": True}


class VisualizationManifest(BaseModel):
    reference: VisualizationReference
    viewport: ViewportReference
    renderer: RendererReference
    theme: Optional[ThemeReference] = None

    model_config = {"extra": "forbid", "frozen": True}
