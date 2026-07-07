"""DOT generator: converts DiagramDefinition to DOT source text."""

from __future__ import annotations

from typing import List
from .models import DiagramDefinition


def build_dot(defn: DiagramDefinition) -> str:
    """Produce a Graphviz DOT source string from a DiagramDefinition."""
    lines: List[str] = ["digraph G {", "  rankdir=LR;"]
    for n in defn.nodes:
        label = n.label.replace('"', "'")
        lines.append(f'  "{n.node_id}" [label="{label}"];')
    for e in defn.edges:
        lbl = f' [label="{e.label}"]' if e.label else ""
        lines.append(f'  "{e.source}" -> "{e.target}"{lbl};')
    lines.append("}")
    return "\n".join(lines)


class DotGenerator:
    """Generate Graphviz DOT source for diagram definitions."""

    def generate(self, definition: DiagramDefinition) -> str:
        return build_dot(definition)


__all__ = ["DotGenerator", "build_dot"]
