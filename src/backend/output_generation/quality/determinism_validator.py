from __future__ import annotations

import hashlib
import logging
import re
from typing import Optional

from .enums import ValidationSeverity, ValidatorName
from .models import DeterminismReport, QualityIssue


class DeterminismValidator:
    """Validate the generated bundle is stable and free of timestamp-based nondeterminism."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def validate(self, bundle: object, approved_snapshot: Optional[object] = None, bundle_version: int = 1) -> DeterminismReport:
        contents = self._extract_texts(bundle)
        fingerprint_source = "\n".join(sorted(contents))
        current_build_hash = hashlib.sha256(fingerprint_source.encode("utf-8")).hexdigest()
        non_deterministic_files = [
            content for content in contents if re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", content)
        ]

        issues: list[QualityIssue] = []
        if non_deterministic_files:
            issues.append(
                QualityIssue(
                    id="QUAL-DET-001",
                    validator=ValidatorName.DETERMINISM,
                    severity=ValidationSeverity.ERROR,
                    title="Timestamp-based nondeterminism detected",
                    description="One or more artifacts contain timestamps that would make regeneration unstable.",
                    remediation="Remove or normalize timestamps before persisting generated artifacts.",
                    is_actionable=True,
                )
            )

        return DeterminismReport(
            determinism_baseline_version=str(bundle_version),
            current_build_hash=current_build_hash,
            files_matching_baseline={},
            non_deterministic_files=non_deterministic_files,
            root_causes=["timestamped content"] if non_deterministic_files else [],
            issues=issues,
            verdict=ValidationSeverity.ERROR if issues else ValidationSeverity.INFO,
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
