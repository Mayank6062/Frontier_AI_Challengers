"""Deployment topology diagram factory."""

from __future__ import annotations

from ..models import DiagramDefinition, DiagramNode


def create_deployment_topology(nodes: list[tuple[str, str]]) -> DiagramDefinition:
    # nodes: list of (node_id, label)
    node_objs = [DiagramNode(node_id=nid, label=lbl) for nid, lbl in nodes]
    return DiagramDefinition(diagram_type="deployment_topology", nodes=node_objs, edges=[])


__all__ = ["create_deployment_topology"]
