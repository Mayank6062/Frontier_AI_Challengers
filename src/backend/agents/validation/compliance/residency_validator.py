from __future__ import annotations

from typing import Any, Dict


def validate_residency(metadata: Any) -> Dict[str, Any]:
    return {"data_residency": "global", "compliant": True}
