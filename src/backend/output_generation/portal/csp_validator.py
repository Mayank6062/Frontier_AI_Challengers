"""Content Security Policy validation for offline portal HTML."""

from __future__ import annotations

from dataclasses import dataclass, field
import re


_CSP_RE = re.compile(
    r"<meta\s+[^>]*http-equiv=[\"']Content-Security-Policy[\"'][^>]*content=[\"']([^\"']+)[\"'][^>]*>",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class CspValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)


class CspValidator:
    """Require a restrictive CSP suitable for offline bundles."""

    def validate(self, html: str) -> CspValidationResult:
        match = _CSP_RE.search(html)
        if not match:
            return CspValidationResult(False, ["missing_csp_meta"])
        policy = match.group(1)
        errors: list[str] = []
        if "default-src 'none'" not in policy:
            errors.append("default_src_not_none")
        if "base-uri 'none'" not in policy:
            errors.append("base_uri_not_none")
        if "object-src 'none'" not in policy:
            errors.append("object_src_not_none")
        if "http:" in policy or "https:" in policy:
            errors.append("external_source_allowed")
        return CspValidationResult(is_valid=not errors, errors=errors)


__all__ = ["CspValidationResult", "CspValidator"]
