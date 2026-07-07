"""Markdown section formatting utilities."""

from __future__ import annotations

import re
from typing import Iterable, Mapping


_ANCHOR_CHARS = re.compile(r"[^a-z0-9 -]")
_WHITESPACE = re.compile(r"\s+")


class SectionFormatter:
    """Build consistent section headings, anchors, and tables."""

    def anchor_for(self, title: str) -> str:
        lowered = _ANCHOR_CHARS.sub("", title.lower())
        return _WHITESPACE.sub("-", lowered).strip("-")

    def heading(self, title: str, level: int = 2) -> str:
        if not 1 <= level <= 6:
            raise ValueError("heading level must be between 1 and 6")
        clean_title = title.strip()
        if not clean_title:
            raise ValueError("heading title must not be empty")
        return f"{'#' * level} {clean_title}"

    def bullet_list(self, items: Iterable[object]) -> str:
        return "\n".join(f"- {str(item).strip()}" for item in items if str(item).strip())

    def table(self, rows: Iterable[Mapping[str, object]], columns: list[str]) -> str:
        if not columns:
            raise ValueError("columns must not be empty")
        header = "| " + " | ".join(columns) + " |"
        divider = "| " + " | ".join("---" for _ in columns) + " |"
        body = [
            "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
            for row in rows
        ]
        return "\n".join([header, divider, *body])


__all__ = ["SectionFormatter"]
