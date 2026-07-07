"""System overview diagram factory."""

from __future__ import annotations

from ..models import DiagramDefinition, DiagramNode, DiagramEdge


def create_system_overview(title: str, components: list[str]) -> DiagramDefinition:
    nodes = [DiagramNode(node_id=c, label=c) for c in components]
    edges: list[DiagramEdge] = []
    return DiagramDefinition(diagram_type="system_overview", nodes=nodes, edges=edges)


__all__ = ["create_system_overview"]
