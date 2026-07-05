from __future__ import annotations

from typing import Optional, Dict, Any


def map_landing_zone(domain: Optional[str] = None) -> Dict[str, Any]:
    """Map a domain to a landing zone profile.

    The mapping is deterministic and returns metadata only.
    """
    if domain and "regulated" in domain.lower():
        return {
            "name": "regulated-zone",
            "controls": ["encryption", "audit"],
            "citation": "knowledge:lz#regulated",
        }
    return {
        "name": "standard-zone",
        "controls": ["monitoring"],
        "citation": "knowledge:lz#standard",
    }
