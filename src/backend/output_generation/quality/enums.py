from __future__ import annotations

import enum

from ..enums import FailureSeverity


class ValidationSeverity(enum.StrEnum):
    BLOCKER = "blocker"
    ERROR = "error"
    WARN = "warn"
    INFO = "info"


class ValidatorName(enum.StrEnum):
    COMPLETENESS = "completeness"
    SEMANTIC = "semantic"
    CITATION = "citation"
    DETERMINISM = "determinism"
    ACCESSIBILITY = "accessibility"
    SECURITY = "security"
    PERFORMANCE = "performance"
    SCORING = "scoring"


# Reuse canonical FailureSeverity for mapping if needed
ValidationSeverityAlias = ValidationSeverity
QualityFailureSeverity = FailureSeverity
