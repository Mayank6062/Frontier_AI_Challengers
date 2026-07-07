from __future__ import annotations

from typing import Protocol, Iterable, Dict
from uuid import UUID

from .models import (
    VisualizationRequest,
    VisualizationResponse,
    VisualizationResult,
    VisualizationDefinition,
)
from .layout import LayoutResult, LayoutConfiguration
from .routing import RoutingResult, RoutingConfiguration
from .collision import CollisionResult
from .legend import LegendDefinition
from .theme import VisualizationTheme
from .responsive import ResponsiveConfiguration
from .zoom import ZoomState


class VisualizationEngine(Protocol):
    def visualize(self, request: VisualizationRequest) -> VisualizationResponse:
        """Produce visualization artifacts for a request."""


class LayoutEngine(Protocol):
    def layout(
        self, definition: VisualizationDefinition, config: LayoutConfiguration
    ) -> LayoutResult:
        """Compute layout for a visualization definition."""


class RoutingEngine(Protocol):
    def route(
        self, layout: LayoutResult, config: RoutingConfiguration
    ) -> RoutingResult:
        """Compute edge routing for a layout."""


class CollisionEngine(Protocol):
    def resolve(self, layout: LayoutResult) -> CollisionResult:
        """Resolve collisions in a layout."""


class LegendEngine(Protocol):
    def build(self, definition: VisualizationDefinition) -> LegendDefinition:
        """Build legend for visualization."""


class ThemeEngine(Protocol):
    def resolve(self, theme_name: str) -> VisualizationTheme:
        """Resolve a theme by name."""


class ResponsiveEngine(Protocol):
    def adapt(self, config: ResponsiveConfiguration) -> None:
        """Adapt visualization to responsive configuration (protocol-only)."""


class ViewportManager(Protocol):
    def current_view(self) -> Dict[str, object]:
        """Return current viewport state."""


class ZoomManager(Protocol):
    def state(self) -> ZoomState:
        """Return zoom state."""


class PanManager(Protocol):
    def state(self) -> Dict[str, object]:
        """Return pan state."""


class ScreenshotEngine(Protocol):
    def capture(self, result: VisualizationResult) -> bytes:
        """Capture screenshot bytes for a visualization result."""


class PrintLayoutEngine(Protocol):
    def layout_for_print(self, result: VisualizationResult) -> VisualizationResult:
        """Produce a print-optimized visualization result."""


class NodeRankingEngine(Protocol):
    def rank(self, definition: VisualizationDefinition) -> Iterable[Dict[str, object]]:
        """Rank nodes by importance."""


class VisualizationFactory(Protocol):
    def create(self, **kwargs: object) -> VisualizationDefinition:
        """Factory method for creating VisualizationDefinition objects."""


class VisualizationRegistry(Protocol):
    def register(self, definition: VisualizationDefinition) -> UUID:
        """Register a visualization and return its id."""


class VisualizationSettingsResolver(Protocol):
    def resolve(self) -> Dict[str, object]:
        """Resolve effective visualization settings."""
