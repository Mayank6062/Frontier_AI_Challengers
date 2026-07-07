"""Self-contained HTML report generator."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..manifest.integrity_hasher import compute_content_hash
from .sanitizer import HtmlSanitizer


@dataclass(frozen=True)
class HtmlArtifact:
    relative_path: str
    media_type: str
    content_bytes: bytes
    size_bytes: int
    content_hash: str


@dataclass(frozen=True)
class HtmlGenerationResult:
    artifacts: list[HtmlArtifact]
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


class ReportGenerator:
    """Render sanitized single-file HTML reports from approved snapshots."""

    def __init__(self, template_dir: str | Path | None = None, sanitizer: HtmlSanitizer | None = None) -> None:
        if template_dir is None:
            template_dir = Path(__file__).with_name("templates")
        self.env = Environment(loader=FileSystemLoader(template_dir), autoescape=select_autoescape(["html", "j2"]))
        self.template = self.env.get_template("report_template.html.j2")
        self.sanitizer = sanitizer or HtmlSanitizer()

    async def generate(self, context: Any) -> HtmlGenerationResult:
        rendered = self.template.render(snapshot=_snapshot_from_context(context))
        sanitized = self.sanitizer.sanitize(rendered)
        content_bytes = sanitized.encode("utf-8")
        artifact = HtmlArtifact(
            relative_path="report.html",
            media_type="text/html",
            content_bytes=content_bytes,
            size_bytes=len(content_bytes),
            content_hash=compute_content_hash(content_bytes),
        )
        return HtmlGenerationResult(
            artifacts=[artifact],
            generator_name="report_generator",
            generator_version=self.get_generator_version(),
        )

    def get_output_file_type(self) -> str:
        return "text/html"

    def get_generator_version(self) -> str:
        return "1.0.0"

    def is_optional(self) -> bool:
        return False


__all__ = ["HtmlArtifact", "HtmlGenerationResult", "ReportGenerator"]
