"""Service mesh diagram factory."""

from __future__ import annotations

from ..models import DiagramDefinition, DiagramNode, DiagramEdge


def create_service_mesh(services: list[str], calls: list[tuple[str, str]]) -> DiagramDefinition:
    nodes = [DiagramNode(node_id=s, label=s) for s in services]
    edges = [DiagramEdge(source=a, target=b) for a, b in calls]
    return DiagramDefinition(diagram_type="service_mesh", nodes=nodes, edges=edges)


__all__ = ["create_service_mesh"]
