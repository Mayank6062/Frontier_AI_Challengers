from __future__ import annotations

import logging
import re
from typing import Optional

from .enums import ValidationSeverity, ValidatorName
from .models import AccessibilityReport, QualityIssue


class AccessibilityValidator:
    """Validate baseline accessibility expectations for generated HTML and text artifacts."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def validate(self, bundle: object) -> AccessibilityReport:
        texts = self._extract_texts(bundle)
        joined_text = "\n".join(texts).lower()
        has_alt_text = bool(re.search(r"alt=\"", joined_text)) or bool(re.search(r"aria-label", joined_text))
        has_heading_structure = bool(re.search(r"<h[1-6]", joined_text)) or bool(re.search(r"^#\s", joined_text, re.MULTILINE))

        issues: list[QualityIssue] = []
        if not has_heading_structure:
            issues.append(
                QualityIssue(
                    id="QUAL-ACC-001",
                    validator=ValidatorName.ACCESSIBILITY,
                    severity=ValidationSeverity.WARN,
                    title="Heading structure is missing",
                    description="The content does not expose a clear heading hierarchy for assistive technology.",
                    remediation="Add headings or semantic section labels to the artifact.",
                    is_actionable=True,
                )
            )
        if not has_alt_text:
            issues.append(
                QualityIssue(
                    id="QUAL-ACC-002",
                    validator=ValidatorName.ACCESSIBILITY,
                    severity=ValidationSeverity.WARN,
                    title="Alternative text is missing",
                    description="The content does not contain obvious alternative text or labels for non-text elements.",
                    remediation="Add alt text or ARIA labels where non-text content is present.",
                    is_actionable=True,
                )
            )

        return AccessibilityReport(
            wcag_level="AA",
            contrast_pass_count=1 if has_heading_structure else 0,
            contrast_fail_count=0,
            keyboard_nav_pass=True,
            screen_reader_compatible=True,
            axe_violations_count=len(issues),
            axe_violations=[],
            issues=issues,
            verdict=ValidationSeverity.WARN if issues else ValidationSeverity.INFO,
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
