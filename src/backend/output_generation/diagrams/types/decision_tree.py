"""Decision tree diagram factory."""

from __future__ import annotations

from ..models import DiagramDefinition, DiagramNode, DiagramEdge


def create_decision_tree(nodes: list[tuple[str, str]], edges: list[tuple[str, str]]) -> DiagramDefinition:
    node_objs = [DiagramNode(node_id=nid, label=lbl) for nid, lbl in nodes]
    edge_objs = [DiagramEdge(source=a, target=b) for a, b in edges]
    return DiagramDefinition(diagram_type="decision_tree", nodes=node_objs, edges=edge_objs)


__all__ = ["create_decision_tree"]
