from __future__ import annotations

from typing import Dict
from pydantic import BaseModel, Field

from .layout import HierarchicalLayoutConfig, ForceLayoutConfig
from .routing import RoutingConfiguration
from .legend import LegendConfiguration
from .theme import VisualizationTheme
from .responsive import ResponsiveConfiguration
from .zoom import ZoomConfiguration
from .print import PrintSettings


class LayoutSettings(BaseModel):
    hierarchical: HierarchicalLayoutConfig = Field(
        default_factory=HierarchicalLayoutConfig
    )
    force: ForceLayoutConfig = Field(default_factory=ForceLayoutConfig)

    model_config = {"extra": "forbid", "frozen": True}


class RoutingSettings(BaseModel):
    default: RoutingConfiguration = Field(default_factory=RoutingConfiguration)

    model_config = {"extra": "forbid", "frozen": True}


class CollisionSettings(BaseModel):
    enabled: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class LegendSettings(BaseModel):
    default: LegendConfiguration = Field(default_factory=LegendConfiguration)

    model_config = {"extra": "forbid", "frozen": True}


class ThemeSettings(BaseModel):
    themes: Dict[str, VisualizationTheme] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class ResponsiveSettings(BaseModel):
    config: ResponsiveConfiguration = Field(default_factory=ResponsiveConfiguration)

    model_config = {"extra": "forbid", "frozen": True}


class ZoomSettings(BaseModel):
    config: ZoomConfiguration = Field(default_factory=ZoomConfiguration)

    model_config = {"extra": "forbid", "frozen": True}


class PerformanceSettings(BaseModel):
    max_nodes_in_memory: int = 500

    model_config = {"extra": "forbid", "frozen": True}


class VisualizationSettings(BaseModel):
    layout: LayoutSettings = Field(default_factory=LayoutSettings)
    routing: RoutingSettings = Field(default_factory=RoutingSettings)
    collision: CollisionSettings = Field(default_factory=CollisionSettings)
    legend: LegendSettings = Field(default_factory=LegendSettings)
    theme: ThemeSettings = Field(default_factory=ThemeSettings)
    responsive: ResponsiveSettings = Field(default_factory=ResponsiveSettings)
    zoom: ZoomSettings = Field(default_factory=ZoomSettings)
    print: PrintSettings = Field(default_factory=PrintSettings)
    performance: PerformanceSettings = Field(default_factory=PerformanceSettings)

    model_config = {"extra": "forbid", "frozen": True}
