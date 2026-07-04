from __future__ import annotations

from pydantic import BaseModel


class PingResponse(BaseModel):
    ok: bool
