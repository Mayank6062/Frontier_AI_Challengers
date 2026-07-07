"""Canonical diagram generation engine."""

from __future__ import annotations

from dataclasses import dataclass

from .diagram_validator import validate_definition
from .dot_generator import DotGenerator
from .mermaid_generator import MermaidGenerator
from .models import DiagramDefinition
from .png_rasterizer import rasterize_png_from_svg
from .svg_renderer import render_svg_from_text


@dataclass(frozen=True)
class DiagramRenderResult:
    mermaid: str
    dot: str
    svg: str
    png: bytes
    validation_errors: list[str]


class DiagramEngine:
    """Generate all canonical diagram representations from one definition."""

    def __init__(self, mermaid: MermaidGenerator | None = None, dot: DotGenerator | None = None) -> None:
        self.mermaid = mermaid or MermaidGenerator()
        self.dot = dot or DotGenerator()

    def render(self, definition: DiagramDefinition) -> DiagramRenderResult:
        validation_errors = validate_definition(definition)
        mermaid_source = self.mermaid.generate(definition)
        dot_source = self.dot.generate(definition)
        title = definition.metadata.title if definition.metadata and definition.metadata.title else definition.diagram_type
        svg = render_svg_from_text(mermaid_source, title=title)
        png = rasterize_png_from_svg(svg.encode("utf-8"))
        return DiagramRenderResult(
            mermaid=mermaid_source,
            dot=dot_source,
            svg=svg,
            png=png,
            validation_errors=validation_errors,
        )


__all__ = ["DiagramEngine", "DiagramRenderResult"]
