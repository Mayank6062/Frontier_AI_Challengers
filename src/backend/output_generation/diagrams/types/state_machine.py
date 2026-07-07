"""State machine diagram factory."""

from __future__ import annotations

from ..models import DiagramDefinition, DiagramNode, DiagramEdge


def create_state_machine(states: list[str], transitions: list[tuple[str, str]]) -> DiagramDefinition:
    nodes = [DiagramNode(node_id=s, label=s) for s in states]
    edges = [DiagramEdge(source=a, target=b) for a, b in transitions]
    return DiagramDefinition(diagram_type="state_machine", nodes=nodes, edges=edges)


__all__ = ["create_state_machine"]
