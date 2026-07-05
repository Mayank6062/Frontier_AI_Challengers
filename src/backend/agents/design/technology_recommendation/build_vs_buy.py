from __future__ import annotations

from typing import Any, List, Dict


def analyze_build_vs_buy(scored: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Simple rule-based build vs buy decision based on vendor maturity and strategic fit."""
    top = scored[0] if scored else None
    if not top:
        return {"decision": "insufficient_data", "reason": "no_candidates"}
    if top.get("maturity", 0) > 0.9 and top.get("fit", 0) > 0.8:
        return {
            "decision": "buy",
            "reason": "proven_off_the_shelf",
            "technology": top.get("name"),
        }
    return {
        "decision": "build",
        "reason": "needs_customization",
        "technology": top.get("name"),
    }
