from __future__ import annotations

from typing import Any, Dict, List


def score_risks(risks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    for r in risks:
        r["score"] = round(r.get("likelihood", 0) * r.get("impact", 0), 3)
    return sorted(risks, key=lambda x: x["score"], reverse=True)
