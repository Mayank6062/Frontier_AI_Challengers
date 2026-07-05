from __future__ import annotations

from typing import Any, Dict, List


def advise_optimizations(estimates: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return straightforward optimization recommendations."""
    annual = estimates.get("annual", 0)
    adv: List[Dict[str, Any]] = []
    if annual > 50000:
        adv.append({"action": "rightsizing", "impact": "medium"})
    else:
        adv.append({"action": "reserved-instances", "impact": "low"})
    return adv
