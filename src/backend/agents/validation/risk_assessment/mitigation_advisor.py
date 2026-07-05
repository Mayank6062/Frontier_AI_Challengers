from __future__ import annotations

from typing import Any, List, Dict


def recommend_mitigations(scored: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    res: List[Dict[str, Any]] = []
    for r in scored:
        if r.get("score", 0) > 0.2:
            res.append(
                {"risk_id": r.get("risk_id"), "mitigation": "apply rate limiting"}
            )
        else:
            res.append({"risk_id": r.get("risk_id"), "mitigation": "monitor"})
    return res
