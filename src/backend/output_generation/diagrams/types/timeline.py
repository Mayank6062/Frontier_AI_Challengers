"""Timeline diagram factory."""

from __future__ import annotations

from ..models import DiagramDefinition, DiagramNode, DiagramEdge


def create_timeline(events: list[tuple[str, str]]) -> DiagramDefinition:
    nodes = [DiagramNode(node_id=str(i), label=lbl) for i, (_, lbl) in enumerate(events)]
    edges: list[DiagramEdge] = []
    return DiagramDefinition(diagram_type="timeline", nodes=nodes, edges=edges)


__all__ = ["create_timeline"]
