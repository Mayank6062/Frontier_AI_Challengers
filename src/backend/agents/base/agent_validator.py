from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .agent_result import AgentResult


@dataclass(frozen=True)
class ValidationResult:
    passed: bool
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]


class AgentValidator:
    """Validate AgentResult instances against simple structural rules.

    This validator is intentionally lightweight and framework-focused.
    """

    def __init__(self, min_confidence: Optional[float] = None) -> None:
        self.min_confidence = min_confidence

    def validate(self, result: AgentResult) -> ValidationResult:
        errors: List[str] = []
        warnings: List[str] = []

        # Confidence must be within [0.0, 1.0] if present
        if result.confidence is not None:
            if not (0.0 <= result.confidence <= 1.0):
                errors.append(f"confidence_out_of_range:{result.confidence}")
            elif (
                self.min_confidence is not None
                and result.confidence < self.min_confidence
            ):
                warnings.append(f"confidence_below_min:{result.confidence}")

        # Payload should be a dict if present
        if result.payload is not None and not isinstance(result.payload, dict):
            errors.append("payload_not_dict")

        # Execution time should be non-negative
        if result.execution_time_ms is not None and result.execution_time_ms < 0:
            errors.append("negative_execution_time")

        # Errors must be strings
        for e in result.errors:
            if not isinstance(e, str):
                errors.append("error_item_not_str")

        # Citations and warnings must be lists of strings
        for c in result.citations:
            if not isinstance(c, str):
                errors.append("citation_item_not_str")

        passed = len(errors) == 0
        metadata: Dict[str, Any] = {"agent_name": result.agent_name}
        return ValidationResult(
            passed=passed, errors=errors, warnings=warnings, metadata=metadata
        )
