"""Edge bundling utilities."""

from __future__ import annotations

from ...output_generation.diagrams.models import DiagramDefinition, DiagramEdge


class EdgeBundler:
    """Group edges by source and target pair."""

    def bundle(self, definition: DiagramDefinition) -> dict[tuple[str, str], list[DiagramEdge]]:
        bundles: dict[tuple[str, str], list[DiagramEdge]] = {}
        for edge in definition.edges:
            bundles.setdefault((edge.source, edge.target), []).append(edge)
        return bundles


__all__ = ["EdgeBundler"]
