from __future__ import annotations

from typing import Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from .theme import VisualizationTheme
from .enums import RendererType


class VisualizationRegistryEntry(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class LayoutRegistryEntry(BaseModel):
    name: str
    algorithm: str
    description: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class ThemeRegistry(BaseModel):
    themes: Dict[str, VisualizationTheme] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class RendererRegistry(BaseModel):
    renderers: Dict[RendererType, str] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class AlgorithmRegistry(BaseModel):
    algorithms: List[str] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}
