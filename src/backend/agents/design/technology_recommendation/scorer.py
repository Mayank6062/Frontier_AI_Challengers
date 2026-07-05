from __future__ import annotations

from typing import Any, List, Dict


def score_technologies(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Attach simple scores to technologies based on maturity and fit.

    This deterministic scorer weights maturity higher than novelty.
    """
    for c in candidates:
        maturity = float(c.get("maturity", 0.5))
        fit = float(c.get("fit", 0.5))
        c["score"] = round(0.6 * maturity + 0.4 * fit, 3)
    return sorted(candidates, key=lambda x: x["score"], reverse=True)
