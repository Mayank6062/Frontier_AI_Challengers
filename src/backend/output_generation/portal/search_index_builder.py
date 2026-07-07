"""Build deterministic offline portal search indexes."""

from __future__ import annotations

from dataclasses import dataclass, field
from html import unescape
import re
from typing import Mapping
from uuid import UUID, uuid4


_TAG_RE = re.compile(r"<[^>]+>")
_SPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class SearchIndexEntry:
    title: str
    path: str
    snippet: str
    section_id: str | None = None
    entry_id: UUID = field(default_factory=uuid4)


class SearchIndexBuilder:
    """Create compact search documents for the self-contained portal."""

    def build(self, sections: list[Mapping[str, object]]) -> list[SearchIndexEntry]:
        entries: list[SearchIndexEntry] = []
        for section in sections:
            title = str(section.get("title") or "Section").strip()
            section_id = str(section.get("id") or section.get("anchor") or title.lower().replace(" ", "-")).strip()
            body = self._clean_text(str(section.get("body") or section.get("description") or ""))
            entries.append(SearchIndexEntry(title=title, path=f"#{section_id}", snippet=body[:240], section_id=section_id))
        return entries

    def _clean_text(self, value: str) -> str:
        return _SPACE_RE.sub(" ", unescape(_TAG_RE.sub(" ", value))).strip()


__all__ = ["SearchIndexBuilder", "SearchIndexEntry"]
