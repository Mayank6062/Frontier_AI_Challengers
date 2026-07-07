"""Split large diagrams into smaller parts based on complexity heuristics."""

from __future__ import annotations

from typing import List
from .models import DiagramDefinition


def split_by_size(defn: DiagramDefinition, max_nodes: int = 50) -> List[DiagramDefinition]:
    """Split a diagram into multiple DiagramDefinition objects if node count exceeds max_nodes.

    This uses a naive chunking strategy based on node order to keep the
    implementation deterministic and simple.
    """
    nodes = defn.nodes
    if len(nodes) <= max_nodes:
        return [defn]
    chunks: List[DiagramDefinition] = []
    for i in range(0, len(nodes), max_nodes):
        subset = nodes[i : i + max_nodes]
        subset_ids = {n.node_id for n in subset}
        edges = [e for e in defn.edges if e.source in subset_ids and e.target in subset_ids]
        chunk = DiagramDefinition(
            diagram_type=defn.diagram_type,
            nodes=subset,
            edges=edges,
            clusters=[c for c in defn.clusters if any(nid in subset_ids for nid in c.nodes)],
            legend=defn.legend,
            metadata=defn.metadata,
            layout=defn.layout,
            accessibility=defn.accessibility,
        )
        chunks.append(chunk)
    return chunks


__all__ = ["split_by_size"]
