"""Component dependency diagram factory."""

from __future__ import annotations

from ..models import DiagramDefinition, DiagramNode, DiagramEdge


def create_component_dependency(components: dict[str, list[str]]) -> DiagramDefinition:
    nodes = [DiagramNode(node_id=k, label=k) for k in components.keys()]
    edges = []
    for src, deps in components.items():
        for d in deps:
            edges.append(DiagramEdge(source=src, target=d))
    return DiagramDefinition(diagram_type="component_dependency", nodes=nodes, edges=edges)


__all__ = ["create_component_dependency"]
