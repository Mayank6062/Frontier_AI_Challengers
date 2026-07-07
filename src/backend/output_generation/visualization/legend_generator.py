"""Legend generation for visualization outputs."""

from __future__ import annotations

from ...output_generation.diagrams.models import DiagramDefinition
from .legend import LegendDefinition, LegendItem


class LegendGenerator:
    """Create legends from diagram node metadata."""

    def generate(self, definition: DiagramDefinition) -> LegendDefinition:
        seen: dict[str, LegendItem] = {}
        for node in definition.nodes:
            kind = node.metadata.get("type") or node.metadata.get("kind")
            if kind and kind not in seen:
                seen[kind] = LegendItem(key=kind, label=kind.replace("_", " ").title())
        return LegendDefinition(items=list(seen.values()))


__all__ = ["LegendGenerator"]
