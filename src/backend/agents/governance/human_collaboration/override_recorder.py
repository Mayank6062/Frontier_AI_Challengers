from __future__ import annotations

from typing import Any, Dict


def record_override(metadata: Any) -> Dict[str, Any]:
    return {"recorded": True, "id": "ovr-1"}
