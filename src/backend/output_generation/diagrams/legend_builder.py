"""Build a legend for a diagram based on node metadata."""

from __future__ import annotations

from typing import Dict
from .models import DiagramDefinition


def build_legend(defn: DiagramDefinition) -> Dict[str, str]:
    """Create a legend mapping from node types found in metadata to labels."""
    legend: Dict[str, str] = {}
    for n in defn.nodes:
        node_type = n.metadata.get("type", "default")
        if node_type not in legend:
            label = n.metadata.get("legend_label", node_type)
            legend[node_type] = label
    return legend


__all__ = ["build_legend"]
