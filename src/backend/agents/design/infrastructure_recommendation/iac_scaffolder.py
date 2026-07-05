from __future__ import annotations

from typing import Any, Dict


def generate_iac_plan(
    topology: Dict[str, Any], landing_zone: Dict[str, Any]
) -> Dict[str, Any]:
    """Produce a minimal IaC plan metadata structure.

    This function returns structured instructions (not actual templates) and
    is intentionally free of SDK or filesystem usage.
    """
    plan = {
        "modules": [
            {"name": "network", "type": "vpc", "count": topology.get("nodes", 1)},
            {
                "name": "compute",
                "type": "vm",
                "count": max(1, topology.get("nodes", 1) * 2),
            },
        ],
        "landing_zone": landing_zone.get("name", "default"),
        "citation": "knowledge:iac#v1",
    }
    return plan
