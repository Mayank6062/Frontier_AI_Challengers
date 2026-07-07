"""Citation formatting helpers for Markdown outputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class Citation:
    citation_id: str
    title: str
    source: str | None = None
    url: str | None = None


class CitationFormatter:
    """Render deterministic Markdown citation lists and inline tags."""

    def inline_tag(self, citation_id: str) -> str:
        clean_id = citation_id.strip()
        if not clean_id:
            raise ValueError("citation_id must not be empty")
        return f"[^{clean_id}]"

    def format_citation(self, citation: Citation | Mapping[str, object]) -> str:
        data = citation if isinstance(citation, Mapping) else citation.__dict__
        citation_id = str(data.get("citation_id") or data.get("id") or "").strip()
        title = str(data.get("title") or "").strip()
        if not citation_id or not title:
            raise ValueError("citation requires citation_id and title")
        source = str(data.get("source") or "").strip()
        url = str(data.get("url") or "").strip()
        suffix = f", {source}" if source else ""
        link = f" {url}" if url else ""
        return f"[^{citation_id}]: {title}{suffix}.{link}".rstrip()

    def format_citations(self, citations: Iterable[Citation | Mapping[str, object]]) -> str:
        return "\n".join(self.format_citation(citation) for citation in citations)


__all__ = ["Citation", "CitationFormatter"]
