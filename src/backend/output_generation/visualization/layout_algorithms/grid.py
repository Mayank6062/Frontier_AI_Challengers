"""Grid layout algorithm."""

from __future__ import annotations

import math

from ...diagrams.models import DiagramDefinition
from ..layout import LayoutResult, NodePosition, Viewport


def grid_layout(definition: DiagramDefinition, cell_width: float = 180.0, cell_height: float = 120.0) -> LayoutResult:
    columns = max(1, math.ceil(math.sqrt(max(len(definition.nodes), 1))))
    positions = [
        NodePosition(node_id=node.node_id, x=(index % columns) * cell_width, y=(index // columns) * cell_height)
        for index, node in enumerate(definition.nodes)
    ]
    rows = max(1, math.ceil(len(definition.nodes) / columns))
    return LayoutResult(
        positions=positions,
        viewport=Viewport(width=int(columns * cell_width + 80), height=int(rows * cell_height + 80)),
    )


__all__ = ["grid_layout"]
