"""Data flow diagram factory."""

from __future__ import annotations

from ..models import DiagramDefinition, DiagramEdge, DiagramNode


def create_data_flow(title: str, flows: list[tuple[str, str, str | None]]) -> DiagramDefinition:
    node_ids: dict[str, DiagramNode] = {}
    edges: list[DiagramEdge] = []
    for source, target, label in flows:
        node_ids.setdefault(source, DiagramNode(node_id=source, label=source))
        node_ids.setdefault(target, DiagramNode(node_id=target, label=target))
        edges.append(DiagramEdge(source=source, target=target, label=label))
    return DiagramDefinition(diagram_type="data_flow", nodes=list(node_ids.values()), edges=edges)


__all__ = ["create_data_flow"]
