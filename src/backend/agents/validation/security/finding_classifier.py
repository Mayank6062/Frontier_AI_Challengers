from __future__ import annotations

from typing import List, Dict, Any


def classify_findings(threats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Classify findings into severity buckets and remediation hints."""
    findings: List[Dict[str, Any]] = []
    for t in threats:
        sev = t.get("severity", "low")
        findings.append(
            {
                "id": t.get("id"),
                "severity": sev,
                "remediation": "Apply control: see control mapping",
            }
        )
    return findings
