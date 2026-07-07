from __future__ import annotations

import logging
import re
from typing import Optional

from .enums import ValidationSeverity, ValidatorName
from .models import CompletenessReport, QualityIssue


class CompletenessValidator:
    """Validate required artifacts and sections are present in a generated bundle."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def validate(self, bundle: object, approved_snapshot: Optional[object] = None) -> CompletenessReport:
        artifacts = self._extract_artifacts(bundle)
        texts = self._extract_texts(bundle)
        joined_text = "\n".join(texts).lower()

        required_files_present = {
            "manifest": any(path.endswith("manifest.json") or "manifest" in path.lower() for path in artifacts),
            "report": any(path.endswith("report.json") or "quality" in path.lower() or "report" in path.lower() for path in artifacts),
            "diagram": any(path.endswith((".mmd", ".svg", ".dot")) for path in artifacts),
            "html": any(path.endswith(".html") for path in artifacts),
        }
        required_sections_present = {
            "executive_summary": bool(re.search(r"executive summary|overview", joined_text)),
            "architecture_summary": bool(re.search(r"architecture|component", joined_text)),
            "risk_register": bool(re.search(r"risk|threat", joined_text)),
        }
        expected_diagram_count = 1 if required_files_present["diagram"] else 0
        actual_diagram_count = sum(1 for path in artifacts if path.endswith((".mmd", ".svg", ".dot")))

        issues: list[QualityIssue] = []
        if not artifacts:
            issues.append(
                QualityIssue(
                    id="QUAL-COMP-001",
                    validator=ValidatorName.COMPLETENESS,
                    severity=ValidationSeverity.BLOCKER,
                    title="No bundle artifacts were found",
                    description="The bundle did not contain any generated artifacts to validate.",
                    remediation="Ensure the generation pipeline produces at least one artifact before quality validation.",
                    is_actionable=True,
                )
            )
        if not any(required_files_present.values()):
            issues.append(
                QualityIssue(
                    id="QUAL-COMP-002",
                    validator=ValidatorName.COMPLETENESS,
                    severity=ValidationSeverity.ERROR,
                    title="Expected output artifacts are missing",
                    description="The bundle did not contain the minimum expected output files.",
                    remediation="Inspect the generation stage and confirm the expected files are written to the bundle.",
                    is_actionable=True,
                )
            )
        if actual_diagram_count < expected_diagram_count:
            issues.append(
                QualityIssue(
                    id="QUAL-COMP-003",
                    validator=ValidatorName.COMPLETENESS,
                    severity=ValidationSeverity.WARN,
                    title="Diagram artifact count is below expectation",
                    description="The expected diagram artifact count was not reached.",
                    remediation="Generate at least one diagram artifact for the bundle.",
                    is_actionable=True,
                )
            )

        verdict = ValidationSeverity.BLOCKER if any(issue.severity == ValidationSeverity.BLOCKER for issue in issues) else ValidationSeverity.ERROR if issues else ValidationSeverity.INFO
        return CompletenessReport(
            required_files_present=required_files_present,
            required_sections_present=required_sections_present,
            expected_diagram_count=expected_diagram_count,
            actual_diagram_count=actual_diagram_count,
            issues=issues,
            verdict=verdict,
        )

    def _extract_artifacts(self, bundle: object) -> list[str]:
        if isinstance(bundle, dict):
            artifacts = bundle.get("artifacts") or bundle.get("files") or []
            if isinstance(artifacts, list):
                return [str(item.get("path") or item.get("name") or item) for item in artifacts if isinstance(item, dict)]
            if isinstance(artifacts, (list, tuple)):
                return [str(item) for item in artifacts]
            return []

        for attr in ("artifacts", "files", "payload"):
            value = getattr(bundle, attr, None)
            if isinstance(value, list):
                return [str(item.path if hasattr(item, "path") else item.name if hasattr(item, "name") else item) for item in value]

        return []

    def _extract_texts(self, bundle: object) -> list[str]:
        if isinstance(bundle, dict):
            payload = bundle.get("content") or bundle.get("text") or []
            if isinstance(payload, list):
                return [str(item) for item in payload]
            if isinstance(payload, str):
                return [payload]

        if hasattr(bundle, "content"):
            content = getattr(bundle, "content")
            if isinstance(content, str):
                return [content]
            if isinstance(content, list):
                return [str(item) for item in content]

        return []
