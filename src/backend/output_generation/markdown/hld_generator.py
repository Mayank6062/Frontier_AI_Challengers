"""High-level design (HLD) Markdown generator."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..manifest.integrity_hasher import compute_content_hash


@dataclass(frozen=True)
class MarkdownArtifact:
    relative_path: str
    media_type: str
    content_bytes: bytes
    size_bytes: int
    content_hash: str


@dataclass(frozen=True)
class MarkdownGenerationResult:
    artifacts: list[MarkdownArtifact]
    generator_name: str
    generator_version: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _snapshot_from_context(context: Any) -> dict[str, Any]:
    snapshot = getattr(context, "approved_snapshot", None)
    if isinstance(snapshot, dict):
        return snapshot
    if isinstance(context, dict):
        candidate = context.get("approved_snapshot", context)
        return candidate if isinstance(candidate, dict) else {"value": candidate}
    request = getattr(context, "request", None)
    reference = getattr(request, "approved_snapshot_reference", None)
    return {"approved_snapshot_reference": reference} if reference else {}


class HLDGenerator:
    """Render HLD Markdown from an approved snapshot."""

    def __init__(self, template_dir: str | Path | None = None) -> None:
        if template_dir is None:
            template_dir = Path(__file__).with_name("templates")
        self.env = Environment(loader=FileSystemLoader(template_dir), autoescape=select_autoescape([]))
        self.template = self.env.get_template("hld_template.md.j2")

    async def generate(self, context: Any) -> MarkdownGenerationResult:
        rendered = self.template.render(snapshot=_snapshot_from_context(context))
        content_bytes = rendered.encode("utf-8")
        artifact = MarkdownArtifact(
            relative_path="hld.md",
            media_type="text/markdown",
            content_bytes=content_bytes,
            size_bytes=len(content_bytes),
            content_hash=compute_content_hash(content_bytes),
        )
        return MarkdownGenerationResult(
            artifacts=[artifact],
            generator_name="hld_generator",
            generator_version=self.get_generator_version(),
        )

    def get_output_file_type(self) -> str:
        return "text/markdown"

    def get_generator_version(self) -> str:
        return "1.0.0"

    def is_optional(self) -> bool:
        return False


__all__ = ["HLDGenerator", "MarkdownArtifact", "MarkdownGenerationResult"]
