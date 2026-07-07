"""Low-level design (LLD) Markdown generator."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..manifest.integrity_hasher import compute_content_hash
from .hld_generator import MarkdownArtifact, MarkdownGenerationResult, _snapshot_from_context


class LLDGenerator:
    """Render LLD Markdown from an approved snapshot."""

    def __init__(self, template_dir: str | Path | None = None) -> None:
        if template_dir is None:
            template_dir = Path(__file__).with_name("templates")
        self.env = Environment(loader=FileSystemLoader(template_dir), autoescape=select_autoescape([]))
        self.template = self.env.get_template("lld_template.md.j2")

    async def generate(self, context: Any) -> MarkdownGenerationResult:
        rendered = self.template.render(snapshot=_snapshot_from_context(context))
        content_bytes = rendered.encode("utf-8")
        artifact = MarkdownArtifact(
            relative_path="lld.md",
            media_type="text/markdown",
            content_bytes=content_bytes,
            size_bytes=len(content_bytes),
            content_hash=compute_content_hash(content_bytes),
        )
        return MarkdownGenerationResult(
            artifacts=[artifact],
            generator_name="lld_generator",
            generator_version=self.get_generator_version(),
        )

    def get_output_file_type(self) -> str:
        return "text/markdown"

    def get_generator_version(self) -> str:
        return "1.0.0"

    def is_optional(self) -> bool:
        return False


__all__ = ["LLDGenerator"]
