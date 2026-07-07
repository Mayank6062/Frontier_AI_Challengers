"""Node ranking utilities."""

from __future__ import annotations

from ...output_generation.diagrams.models import DiagramDefinition
from .ranking import NodeRank


class NodeRanker:
    """Rank nodes by graph degree."""

    def rank(self, definition: DiagramDefinition) -> list[NodeRank]:
        degree = {node.node_id: 0 for node in definition.nodes}
        for edge in definition.edges:
            if edge.source in degree:
                degree[edge.source] += 1
            if edge.target in degree:
                degree[edge.target] += 1
        return [NodeRank(node_id=node_id, score=float(score)) for node_id, score in sorted(degree.items())]


__all__ = ["NodeRanker"]
