from __future__ import annotations

from typing import Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class VisualizationTokens(BaseModel):
    tokens: Dict[str, str] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class ColorPalette(BaseModel):
    primary: Optional[str] = None
    secondary: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class TypographyScale(BaseModel):
    base: int = 14
    scale: Dict[str, int] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class DiagramPalette(BaseModel):
    node_fill: Dict[str, str] = Field(default_factory=dict)
    edge_stroke: Dict[str, str] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class VisualizationTheme(BaseModel):
    theme_id: UUID = Field(default_factory=uuid4)
    name: str
    tokens: VisualizationTokens = Field(default_factory=VisualizationTokens)
    colors: ColorPalette = Field(default_factory=ColorPalette)
    typography: TypographyScale = Field(default_factory=TypographyScale)

    model_config = {"extra": "forbid", "frozen": True}


class ResponsiveTheme(BaseModel):
    rules: Dict[str, str] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class PrintTheme(BaseModel):
    high_contrast: bool = True

    model_config = {"extra": "forbid", "frozen": True}
