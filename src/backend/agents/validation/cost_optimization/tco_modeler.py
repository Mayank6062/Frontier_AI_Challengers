from __future__ import annotations

from typing import Any, Dict


def model_tco(metadata: Any) -> Dict[str, Any]:
    """Return a simple TCO model with deterministic outputs."""
    return {"3y": 100000, "5y": 150000, "citation": "knowledge:tco#simple"}
