"""Risk heatmap diagram factory."""

from __future__ import annotations

from ..models import DiagramDefinition, DiagramEdge, DiagramNode


def create_risk_heatmap(title: str, risks: list[dict[str, object]]) -> DiagramDefinition:
    nodes = [
        DiagramNode(
            node_id=str(risk.get("id") or risk.get("title") or index),
            label=f"{risk.get('title', 'Risk')} ({risk.get('severity', 'unrated')})",
            metadata={key: str(value) for key, value in risk.items()},
        )
        for index, risk in enumerate(risks, start=1)
    ]
    return DiagramDefinition(diagram_type="risk_heatmap", nodes=nodes, edges=list[DiagramEdge]())


__all__ = ["create_risk_heatmap"]
