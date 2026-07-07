"""Canonical models for the Portal package (contracts-only).

This file re-exports the immutable Pydantic models defined in the
per-surface files (state.py, router.py, search.py, section.py,
layout.py, theme.py, tokens.py, accessibility.py, command_palette.py,
explorer.py). No implementations are added here — this module centralizes
the package's model surface for importers.
"""

from __future__ import annotations

from .state import PortalState
from .router import PortalRoute, RouteMatch
from .search import SearchIndex, SearchEntry
from .section import (
    SectionRenderContract,
)
from .layout import LayoutModel, TopBar, LeftRail, Inspector, MainCanvas, MiniMap
from .theme import ThemeMetadata, ThemeSettings
from .tokens import AnimationToken
from .accessibility import ARIA, KeyboardMap
from .command_palette import CommandEntry
from .explorer import (
    ArchitectureExplorerState,
    DependencyExplorerState,
    RiskExplorerState,
    CitationExplorerState,
    TimelineExplorerState,
    ExplorerRegistry,
)

__all__ = [
    "PortalState",
    "PortalRoute",
    "RouteMatch",
    "SearchIndex",
    "SearchEntry",
    "SectionRenderContract",
    "LayoutModel",
    "TopBar",
    "LeftRail",
    "Inspector",
    "MainCanvas",
    "MiniMap",
    "ThemeMetadata",
    "ThemeSettings",
    "AnimationToken",
    "ARIA",
    "KeyboardMap",
    "CommandEntry",
    "ArchitectureExplorerState",
    "DependencyExplorerState",
    "RiskExplorerState",
    "CitationExplorerState",
    "TimelineExplorerState",
    "ExplorerRegistry",
]
