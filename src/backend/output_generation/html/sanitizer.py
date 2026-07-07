"""HTML sanitizer for generated reports and portal fragments."""

from __future__ import annotations

from html import escape
from html.parser import HTMLParser
from typing import Final
from urllib.parse import urlparse


_ALLOWED_TAGS: Final[set[str]] = {
    "a",
    "article",
    "aside",
    "body",
    "br",
    "caption",
    "code",
    "dd",
    "div",
    "dl",
    "dt",
    "em",
    "footer",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "header",
    "html",
    "li",
    "main",
    "meta",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "span",
    "strong",
    "style",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "title",
    "tr",
    "ul",
}
_VOID_TAGS: Final[set[str]] = {"br", "meta"}
_ALLOWED_ATTRS: Final[dict[str, set[str]]] = {
    "*": {"aria-label", "aria-labelledby", "class", "data-section", "id", "role"},
    "a": {"href", "title"},
    "meta": {"content", "http-equiv", "name"},
}
_SAFE_SCHEMES: Final[set[str]] = {"", "mailto"}


class _SanitizingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.output: list[str] = []
        self._blocked_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"script", "iframe", "object", "embed", "link"}:
            self._blocked_depth += 1
            return
        if self._blocked_depth or tag not in _ALLOWED_TAGS:
            return
        clean_attrs = self._clean_attrs(tag, attrs)
        suffix = "" if not clean_attrs else " " + " ".join(clean_attrs)
        self.output.append(f"<{tag}{suffix}>")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "iframe", "object", "embed", "link"}:
            self._blocked_depth = max(0, self._blocked_depth - 1)
            return
        if self._blocked_depth or tag not in _ALLOWED_TAGS or tag in _VOID_TAGS:
            return
        self.output.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if not self._blocked_depth:
            self.output.append(escape(data, quote=False))

    def handle_entityref(self, name: str) -> None:
        if not self._blocked_depth:
            self.output.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if not self._blocked_depth:
            self.output.append(f"&#{name};")

    def _clean_attrs(self, tag: str, attrs: list[tuple[str, str | None]]) -> list[str]:
        allowed = _ALLOWED_ATTRS.get("*", set()) | _ALLOWED_ATTRS.get(tag, set())
        clean: list[str] = []
        for name, value in attrs:
            attr = name.lower()
            if attr.startswith("on") or attr not in allowed:
                continue
            safe_value = "" if value is None else value
            if attr == "href" and not self._safe_href(safe_value):
                continue
            clean.append(f'{attr}="{escape(safe_value, quote=True)}"')
        return clean

    def _safe_href(self, value: str) -> bool:
        parsed = urlparse(value.strip())
        return parsed.scheme.lower() in _SAFE_SCHEMES and not value.strip().startswith("//")


class HtmlSanitizer:
    """Allowlist-based sanitizer with no external runtime dependency."""

    def sanitize(self, html: str) -> str:
        parser = _SanitizingParser()
        parser.feed(html)
        parser.close()
        return "".join(parser.output)


__all__ = ["HtmlSanitizer"]
