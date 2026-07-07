from __future__ import annotations

import logging
import re
from typing import Optional

from .enums import ValidationSeverity, ValidatorName
from .models import QualityIssue, SemanticReport


class SemanticValidator:
    """Validate that the generated content contains substantive, justified claims."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def validate(self, bundle: object, approved_snapshot: Optional[object] = None) -> SemanticReport:
        texts = self._extract_texts(bundle)
        joined_text = "\n".join(texts).lower()
        claim_matches = re.findall(r"\b(must|should|will|ensures|provides|supports|requires)\b", joined_text)
        total_claims = len(claim_matches)
        claims_with_justification = sum(
            1
            for match in claim_matches
            if "evidence" in joined_text or "citation" in joined_text or "source" in joined_text
        )
        claims_without_justification = max(total_claims - claims_with_justification, 0)

        issues: list[QualityIssue] = []
        if total_claims == 0:
            issues.append(
                QualityIssue(
                    id="QUAL-SEM-001",
                    validator=ValidatorName.SEMANTIC,
                    severity=ValidationSeverity.WARN,
                    title="No substantive claims detected",
                    description="The generated bundle does not appear to contain substantive claims for validation.",
                    remediation="Ensure the artifact content contains concrete architecture or delivery statements.",
                    is_actionable=True,
                )
            )
        if claims_without_justification:
            issues.append(
                QualityIssue(
                    id="QUAL-SEM-002",
                    validator=ValidatorName.SEMANTIC,
                    severity=ValidationSeverity.ERROR,
                    title="Claims without supporting evidence",
                    description="Some claims appear to lack supporting evidence or citations.",
                    remediation="Add evidence, citations, or references for each important claim.",
                    is_actionable=True,
                )
            )

        verdict = ValidationSeverity.ERROR if issues else ValidationSeverity.INFO
        return SemanticReport(
            total_claims=total_claims,
            claims_with_justification=claims_with_justification,
            claims_without_justification=claims_without_justification,
            circular_dependencies_detected=[],
            issues=issues,
            verdict=verdict,
        )

    def _extract_texts(self, bundle: object) -> list[str]:
        if isinstance(bundle, dict):
            payload = bundle.get("content") or bundle.get("text") or []
            if isinstance(payload, list):
                return [str(item) for item in payload]
            if isinstance(payload, str):
                return [payload]

        content = getattr(bundle, "content", None)
        if isinstance(content, str):
            return [content]
        if isinstance(content, list):
            return [str(item) for item in content]
        return []
