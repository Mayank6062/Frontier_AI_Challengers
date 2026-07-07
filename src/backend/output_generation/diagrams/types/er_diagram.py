"""ER diagram factory."""

from __future__ import annotations

from ..models import DiagramDefinition, DiagramNode, DiagramEdge


def create_er_diagram(entities: list[str], relations: list[tuple[str, str]]) -> DiagramDefinition:
    nodes = [DiagramNode(node_id=e, label=e) for e in entities]
    edges = [DiagramEdge(source=a, target=b) for a, b in relations]
    return DiagramDefinition(diagram_type="er_diagram", nodes=nodes, edges=edges)


__all__ = ["create_er_diagram"]
