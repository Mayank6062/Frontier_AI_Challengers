"""Build accessibility specifications for diagrams."""

from __future__ import annotations

from typing import Dict
from .models import DiagramDefinition


def build_accessibility(defn: DiagramDefinition) -> Dict[str, str]:
    """Construct alt_text and long_description from the definition."""
    title = defn.metadata.title if defn.metadata and defn.metadata.title else "Diagram"
    node_count = len(defn.nodes)
    edge_count = len(defn.edges)
    alt_text = f"{title}: {node_count} nodes, {edge_count} edges"
    long_description = defn.metadata.description if defn.metadata and defn.metadata.description else alt_text
    return {"alt_text": alt_text, "long_description": long_description}


__all__ = ["build_accessibility"]
