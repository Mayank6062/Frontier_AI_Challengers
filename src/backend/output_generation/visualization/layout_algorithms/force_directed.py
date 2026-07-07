"""Deterministic force-directed layout approximation."""

from __future__ import annotations

import math

from ...diagrams.models import DiagramDefinition
from ..layout import LayoutResult, NodePosition, Viewport


def force_directed_layout(definition: DiagramDefinition, radius: float = 220.0) -> LayoutResult:
    total = max(len(definition.nodes), 1)
    positions = [
        NodePosition(
            node_id=node.node_id,
            x=radius + math.cos((2 * math.pi * index) / total) * radius,
            y=radius + math.sin((2 * math.pi * index) / total) * radius,
        )
        for index, node in enumerate(definition.nodes)
    ]
    size = int(radius * 2 + 80)
    return LayoutResult(positions=positions, viewport=Viewport(width=size, height=size))


__all__ = ["force_directed_layout"]
