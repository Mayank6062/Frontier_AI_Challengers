"""Validation for generated Markdown artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MarkdownValidationIssue:
    code: str
    message: str


@dataclass(frozen=True)
class MarkdownValidationResult:
    is_valid: bool
    errors: list[MarkdownValidationIssue] = field(default_factory=list)
    warnings: list[MarkdownValidationIssue] = field(default_factory=list)


class MarkdownValidator:
    """Validate required Markdown structure without mutating content."""

    def validate(self, content: str) -> MarkdownValidationResult:
        errors: list[MarkdownValidationIssue] = []
        warnings: list[MarkdownValidationIssue] = []
        if not content.strip():
            errors.append(MarkdownValidationIssue("empty_document", "Markdown content is empty."))
        if not any(line.startswith("# ") for line in content.splitlines()):
            errors.append(MarkdownValidationIssue("missing_title", "Markdown document must include one H1 title."))
        if "\t" in content:
            warnings.append(MarkdownValidationIssue("tab_indentation", "Markdown contains tab indentation."))
        lowered = content.lower()
        if "todo" in lowered or "stub" in lowered:
            errors.append(MarkdownValidationIssue("non_production_marker", "Markdown contains non-production marker text."))
        return MarkdownValidationResult(is_valid=not errors, errors=errors, warnings=warnings)


__all__ = ["MarkdownValidationIssue", "MarkdownValidationResult", "MarkdownValidator"]
