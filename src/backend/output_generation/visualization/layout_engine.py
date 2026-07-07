"""Canonical visualization layout engine."""

from __future__ import annotations

from ...output_generation.diagrams.models import DiagramDefinition
from .enums import LayoutAlgorithm
from .layout import LayoutConfiguration, LayoutMetadata, LayoutResult
from .layout_algorithms import force_directed_layout, grid_layout, hierarchical_layout, radial_layout, route_orthogonal_edges


class LayoutEngine:
    """Apply deterministic layout algorithms to diagram definitions."""

    def layout(self, definition: DiagramDefinition, configuration: LayoutConfiguration | None = None) -> LayoutResult:
        configuration = configuration or LayoutConfiguration()
        if configuration.algorithm == LayoutAlgorithm.FORCE_DIRECTED:
            result = force_directed_layout(definition)
        elif configuration.algorithm == LayoutAlgorithm.RADIAL:
            result = radial_layout(definition)
        elif configuration.algorithm == LayoutAlgorithm.GRID:
            result = grid_layout(definition)
        else:
            result = hierarchical_layout(definition)
        result = result.model_copy(
            update={
                "routes": route_orthogonal_edges(definition, result.positions),
                "metadata": LayoutMetadata(algorithm=configuration.algorithm, computed_at=0.0),
            }
        )
        return result


__all__ = ["LayoutEngine"]
