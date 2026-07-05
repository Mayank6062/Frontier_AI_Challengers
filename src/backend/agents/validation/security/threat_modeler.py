from __future__ import annotations

from typing import Any, Dict, List


def generate_threat_model(artifact: Any) -> List[Dict[str, Any]]:
    """Derive a list of potential threats for an artifact.

    This is a deterministic implementation for testability.
    """
    threats = [
        {
            "id": "T01",
            "description": "Data exfiltration",
            "severity": "high",
            "citation": "knowledge:threats#data-exfil",
        },
        {
            "id": "T02",
            "description": "Privilege escalation",
            "severity": "medium",
            "citation": "knowledge:threats#priv-esc",
        },
    ]
    return threats
