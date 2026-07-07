"""Offline portal builder."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..manifest.integrity_hasher import compute_content_hash
from .portal_validator import PortalValidator
from .routes import RouteRegistry
from .search_index_builder import SearchIndexBuilder
from .section_renderer import SectionRenderer
from .state_initializer import StateInitializer


@dataclass(frozen=True)
class PortalArtifact:
    relative_path: str
    media_type: str
    content_bytes: bytes
    size_bytes: int
    content_hash: str


@dataclass(frozen=True)
class PortalBuildResult:
    artifacts: list[PortalArtifact]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class PortalBuilder:
    """Build a self-contained offline portal artifact."""

    def __init__(self, template_dir: str | Path | None = None) -> None:
        if template_dir is None:
            template_dir = Path(__file__).with_name("templates")
        self.env = Environment(loader=FileSystemLoader(template_dir), autoescape=select_autoescape(["html", "j2"]))
        self.template = self.env.get_template("base.html.j2")
        self.routes = RouteRegistry()
        self.state_initializer = StateInitializer()
        self.section_renderer = SectionRenderer()
        self.search_index_builder = SearchIndexBuilder()
        self.validator = PortalValidator()

    def build(self, snapshot: Mapping[str, object]) -> PortalBuildResult:
        sections = snapshot.get("sections")
        normalized_sections = sections if isinstance(sections, list) else self._sections_from_snapshot(snapshot)
        html = self.template.render(
            routes=self.routes.list_routes(),
            state=self.state_initializer.initialize(),
            sections_html=self.section_renderer.render_sections(normalized_sections),
            search_index=self.search_index_builder.build(normalized_sections),
            snapshot=snapshot,
        )
        validation = self.validator.validate(html)
        content_bytes = html.encode("utf-8")
        artifact = PortalArtifact(
            relative_path="portal/index.html",
            media_type="text/html",
            content_bytes=content_bytes,
            size_bytes=len(content_bytes),
            content_hash=compute_content_hash(content_bytes),
        )
        return PortalBuildResult(artifacts=[artifact], errors=validation.errors)

    def _sections_from_snapshot(self, snapshot: Mapping[str, object]) -> list[Mapping[str, object]]:
        return [
            {"id": "architecture", "title": "Architecture", "body": snapshot.get("summary", "Architecture snapshot accepted.")},
            {"id": "risks", "title": "Risks", "body": "Risk information is rendered from the approved snapshot."},
            {"id": "citations", "title": "Citations", "body": "Citation information is rendered from the approved snapshot."},
        ]


__all__ = ["PortalArtifact", "PortalBuildResult", "PortalBuilder"]
