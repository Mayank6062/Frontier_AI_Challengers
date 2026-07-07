from __future__ import annotations

import logging
import re
from typing import Optional

from .enums import ValidationSeverity, ValidatorName
from .models import CitationReport, QualityIssue


class CitationValidator:
    """Validate citation coverage and resolve references against available citation data."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def validate(self, bundle: object, approved_snapshot: Optional[object] = None) -> CitationReport:
        texts = self._extract_texts(bundle)
        joined_text = "\n".join(texts)
        cited_ids = re.findall(r"\b(?:CIT|cit)-?[A-Za-z0-9_-]+\b", joined_text)
        citation_index = self._extract_citation_index(bundle, approved_snapshot)
        unresolved = [identifier for identifier in cited_ids if identifier not in citation_index]

        total_citations_in_output = len(cited_ids)
        total_citations_in_snapshot = len(citation_index)
        citations_resolved = total_citations_in_output - len(unresolved)
        citations_unresolved = len(unresolved)
        coverage_percent = 100.0 if total_citations_in_output == 0 else (citations_resolved / total_citations_in_output) * 100.0

        issues: list[QualityIssue] = []
        if total_citations_in_output and citations_unresolved:
            issues.append(
                QualityIssue(
                    id="QUAL-CIT-001",
                    validator=ValidatorName.CITATION,
                    severity=ValidationSeverity.ERROR,
                    title="Unresolved citations detected",
                    description="Some citations referenced in the bundle could not be resolved against the available citation index.",
                    remediation="Ensure every citation ID resolves to an entry in the citation index.",
                    is_actionable=True,
                )
            )

        verdict = ValidationSeverity.ERROR if issues else ValidationSeverity.INFO
        return CitationReport(
            total_citations_in_output=total_citations_in_output,
            total_citations_in_snapshot=total_citations_in_snapshot,
            citations_resolved=citations_resolved,
            citations_unresolved=citations_unresolved,
            coverage_percent=coverage_percent,
            unresolved_citations=unresolved,
            issues=issues,
            verdict=verdict,
        )

    def _extract_citation_index(self, bundle: object, approved_snapshot: Optional[object]) -> set[str]:
        lookup: set[str] = set()
        if isinstance(bundle, dict):
            citation_index = bundle.get("citation_index") or bundle.get("references") or []
            if isinstance(citation_index, list):
                lookup.update(str(item) for item in citation_index)
            elif isinstance(citation_index, dict):
                lookup.update(str(key) for key in citation_index.keys())

        if approved_snapshot is not None:
            snapshot_index = getattr(approved_snapshot, "citation_index", None)
            if isinstance(snapshot_index, list):
                lookup.update(str(item) for item in snapshot_index)
            elif isinstance(snapshot_index, dict):
                lookup.update(str(key) for key in snapshot_index.keys())

        return lookup

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
