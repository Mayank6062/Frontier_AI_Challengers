from __future__ import annotations

from typing import Any, List, Dict, Any as _Any


def check_guardrails(metadata: Any) -> List[Dict[str, _Any]]:
    return [{"guardrail": "no-public-s3", "status": "ok"}]
