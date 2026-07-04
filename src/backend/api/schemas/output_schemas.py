from __future__ import annotations

from pydantic import BaseModel
from typing import Any


class OutputRequest(BaseModel):
    payload: dict[str, Any]


class OutputResponse(BaseModel):
    status: str
