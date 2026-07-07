"""Validation for generated HTML documents."""

from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser


@dataclass(frozen=True)
class HtmlValidationIssue:
    code: str
    message: str


@dataclass(frozen=True)
class HtmlValidationResult:
    is_valid: bool
    errors: list[HtmlValidationIssue] = field(default_factory=list)
    warnings: list[HtmlValidationIssue] = field(default_factory=list)


class _StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.external_urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag.lower())
        for name, value in attrs:
            if name.lower() in {"href", "src"} and value and value.startswith(("http://", "https://", "//")):
                self.external_urls.append(value)


class HtmlValidator:
    """Validate security and structure constraints for generated HTML."""

    def validate(self, html: str) -> HtmlValidationResult:
        errors: list[HtmlValidationIssue] = []
        warnings: list[HtmlValidationIssue] = []
        parser = _StructureParser()
        parser.feed(html)
        if "html" not in parser.tags:
            errors.append(HtmlValidationIssue("missing_html", "Document must include an html element."))
        if "title" not in parser.tags:
            warnings.append(HtmlValidationIssue("missing_title", "Document should include a title element."))
        lowered = html.lower()
        if "<script" in lowered or "javascript:" in lowered or " onerror=" in lowered or " onclick=" in lowered:
            errors.append(HtmlValidationIssue("unsafe_script_surface", "Document contains an unsafe script surface."))
        if parser.external_urls:
            errors.append(HtmlValidationIssue("external_url", "Document must not reference external URLs."))
        return HtmlValidationResult(is_valid=not errors, errors=errors, warnings=warnings)


__all__ = ["HtmlValidationIssue", "HtmlValidationResult", "HtmlValidator"]
