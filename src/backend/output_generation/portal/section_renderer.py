"""Portal section renderer."""

from __future__ import annotations

from html import escape
from typing import Mapping


class SectionRenderer:
    """Render approved snapshot sections into offline HTML fragments."""

    def render_section(self, section: Mapping[str, object]) -> str:
        section_id = escape(str(section.get("id") or section.get("anchor") or "section"), quote=True)
        title = escape(str(section.get("title") or "Section"))
        body = escape(str(section.get("body") or section.get("description") or "Content derived from approved snapshot."))
        return f'<section id="{section_id}" data-section="{section_id}"><h2>{title}</h2><p>{body}</p></section>'

    def render_sections(self, sections: list[Mapping[str, object]]) -> str:
        return "\n".join(self.render_section(section) for section in sections)


__all__ = ["SectionRenderer"]
