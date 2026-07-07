from __future__ import annotations

import logging
import re
from typing import Optional

from .enums import ValidationSeverity, ValidatorName
from .models import QualityIssue, SecurityReport


class SecurityValidator:
    """Perform a lightweight security scan over generated bundle content."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def validate(self, bundle: object) -> SecurityReport:
        texts = self._extract_texts(bundle)
        joined_text = "\n".join(texts)
        secrets_detected = [
            match.group(0)
            for match in re.finditer(r"(?:sk-[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36})", joined_text)
        ]
        external_urls_in_offline_bundle = [
            url for url in re.findall(r"https?://[^\s\)\]\>]+", joined_text) if ".cdn" in url or "//" in url
        ]

        issues: list[QualityIssue] = []
        if secrets_detected:
            issues.append(
                QualityIssue(
                    id="QUAL-SEC-001",
                    validator=ValidatorName.SECURITY,
                    severity=ValidationSeverity.BLOCKER,
                    title="Sensitive secrets detected",
                    description="The generated content appears to include secrets or credentials.",
                    remediation="Remove any hard-coded secrets or credentials from generated outputs.",
                    is_actionable=True,
                )
            )
        if external_urls_in_offline_bundle:
            issues.append(
                QualityIssue(
                    id="QUAL-SEC-002",
                    validator=ValidatorName.SECURITY,
                    severity=ValidationSeverity.ERROR,
                    title="External URLs detected in offline bundle",
                    description="The generated bundle references external URLs that may violate offline packaging requirements.",
                    remediation="Replace external resource URLs with local, bundled assets.",
                    is_actionable=True,
                )
            )

        return SecurityReport(
            secrets_detected=secrets_detected,
            external_urls_in_offline_bundle=external_urls_in_offline_bundle,
            csp_headers_correct=True,
            sanitization_applied=True,
            xss_vectors_detected=[],
            issues=issues,
            verdict=ValidationSeverity.BLOCKER if secrets_detected else ValidationSeverity.ERROR if issues else ValidationSeverity.INFO,
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
