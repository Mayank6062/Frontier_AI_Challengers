from __future__ import annotations

from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class OAuthToken:
    access_token: str
    token_type: str
    scope: Optional[str]
    expires_in: Optional[int]


@dataclass(frozen=True)
class AuthTokenPayload:
    sub: str
    iat: int
    exp: int
