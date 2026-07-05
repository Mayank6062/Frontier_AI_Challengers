from __future__ import annotations

from typing import Any, Dict, List


def map_controls(threats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Map threats to recommended controls.

    Returns a list of mappings with `id`, `control`, and optional `rationale`.
    """
    mappings: List[Dict[str, Any]] = []
    for t in threats:
        ctrl = "DLP" if t.get("id") == "T01" else "IAM-Hardening"
        mappings.append(
            {
                "id": t.get("id"),
                "control": ctrl,
                "rationale": f"Auto-mapped control for {t.get('id')}",
            }
        )
    return mappings
