"""Offline validation for generated portal HTML."""

from __future__ import annotations

from dataclasses import dataclass, field
import re


_EXTERNAL_RE = re.compile(r"""(?:href|src)=["'](?:https?:)?//""", re.IGNORECASE)


@dataclass(frozen=True)
class OfflineValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)


class OfflineValidator:
    """Ensure portal HTML has no network resource dependencies."""

    def validate(self, html: str) -> OfflineValidationResult:
        errors: list[str] = []
        if _EXTERNAL_RE.search(html):
            errors.append("external_resource_reference")
        if "eval(" in html:
            errors.append("eval_usage")
        return OfflineValidationResult(is_valid=not errors, errors=errors)


__all__ = ["OfflineValidationResult", "OfflineValidator"]
