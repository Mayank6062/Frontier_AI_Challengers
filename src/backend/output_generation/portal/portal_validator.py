"""Composite portal validator."""

from __future__ import annotations

from dataclasses import dataclass, field

from .csp_validator import CspValidator
from .offline_validator import OfflineValidator


@dataclass(frozen=True)
class PortalValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)


class PortalValidator:
    """Run portal validators required by Chapter 18."""

    def __init__(self, csp_validator: CspValidator | None = None, offline_validator: OfflineValidator | None = None) -> None:
        self.csp_validator = csp_validator or CspValidator()
        self.offline_validator = offline_validator or OfflineValidator()

    def validate(self, html: str) -> PortalValidationResult:
        errors: list[str] = []
        csp = self.csp_validator.validate(html)
        offline = self.offline_validator.validate(html)
        errors.extend(csp.errors)
        errors.extend(offline.errors)
        if "<main" not in html:
            errors.append("missing_main_region")
        return PortalValidationResult(is_valid=not errors, errors=errors)


__all__ = ["PortalValidationResult", "PortalValidator"]
