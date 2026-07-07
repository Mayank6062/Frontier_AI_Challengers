"""Sequence diagram factory."""

from __future__ import annotations

from ..models import DiagramDefinition, DiagramNode, DiagramEdge


def create_sequence_diagram(participants: list[str], interactions: list[tuple[str, str, str]]) -> DiagramDefinition:
    nodes = [DiagramNode(node_id=p, label=p) for p in participants]
    edges = [DiagramEdge(source=s, target=t, label=lbl) for s, t, lbl in interactions]
    return DiagramDefinition(diagram_type="sequence_diagram", nodes=nodes, edges=edges)


__all__ = ["create_sequence_diagram"]
