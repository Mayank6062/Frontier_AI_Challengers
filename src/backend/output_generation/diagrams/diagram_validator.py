"""Diagram validator: ensure diagram definitions are consistent and valid."""

from __future__ import annotations

from typing import List
from .models import DiagramDefinition


class DiagramValidationError(Exception):
    pass


def validate_definition(defn: DiagramDefinition) -> List[str]:
    """Return a list of validation error codes (empty if valid)."""
    errs: List[str] = []
    ids = {n.node_id for n in defn.nodes}
    if len(ids) != len(defn.nodes):
        errs.append("duplicate_node_id")
    for e in defn.edges:
        if e.source not in ids:
            errs.append(f"edge_source_missing:{e.source}")
        if e.target not in ids:
            errs.append(f"edge_target_missing:{e.target}")
    # simple empty check
    if not defn.nodes:
        errs.append("no_nodes")
    return errs


__all__ = ["validate_definition", "DiagramValidationError"]
