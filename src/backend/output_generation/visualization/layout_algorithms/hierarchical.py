"""Hierarchical layout algorithm."""

from __future__ import annotations

from ...diagrams.models import DiagramDefinition
from ..layout import LayoutResult, NodePosition, Viewport


def hierarchical_layout(definition: DiagramDefinition, x_gap: float = 180.0, y_gap: float = 120.0) -> LayoutResult:
    positions = [NodePosition(node_id=node.node_id, x=index * x_gap, y=(index % 3) * y_gap) for index, node in enumerate(definition.nodes)]
    width = int(max((position.x for position in positions), default=0) + x_gap)
    height = int(max((position.y for position in positions), default=0) + y_gap)
    return LayoutResult(positions=positions, viewport=Viewport(width=max(width, 320), height=max(height, 240)))


__all__ = ["hierarchical_layout"]
