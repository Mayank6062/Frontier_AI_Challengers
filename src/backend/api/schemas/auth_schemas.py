from __future__ import annotations

from pydantic import BaseModel


class TokenRequest(BaseModel):
    username: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
