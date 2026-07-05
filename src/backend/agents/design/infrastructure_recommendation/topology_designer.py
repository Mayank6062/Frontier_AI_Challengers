from __future__ import annotations

from typing import Optional, Dict, Any


def design_topology(domain: Optional[str] = None) -> Dict[str, Any]:
    """Return a simple topology recommendation driven by domain size."""
    if domain and "enterprise" in domain.lower():
        topo = {
            "type": "multi-region",
            "nodes": 5,
            "citation": "knowledge:topologies#multi-region",
        }
    else:
        topo = {
            "type": "single-region",
            "nodes": 2,
            "citation": "knowledge:topologies#single-region",
        }
    return topo
