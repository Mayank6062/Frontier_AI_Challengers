from __future__ import annotations

from typing import Any, List, Dict


def aggregate_risks(metadata: Any) -> List[Dict[str, Any]]:
    return [
        {
            "risk_id": "R1",
            "description": "Operational overload",
            "likelihood": 0.2,
            "impact": 0.6,
        }
    ]
