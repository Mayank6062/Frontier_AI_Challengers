from __future__ import annotations

import time
import hmac
import hashlib
import base64
import json
from typing import Dict, Any, cast


class TokenError(Exception):
    pass


class TokenManager:
    """Simple HMAC-based token manager for issuing and validating opaque tokens.

    Production callers should inject a strong secret via constructor. Tokens
    are compact JSON payloads signed with HMAC-SHA256 and base64-encoded.
    """

    def __init__(self, secret: bytes, algorithm: str = "HS256") -> None:
        if not secret:
            raise ValueError("secret is required")
        self._secret = secret
        self._alg = algorithm

    def _sign(self, payload: bytes) -> str:
        sig = hmac.new(self._secret, payload, hashlib.sha256).digest()
        return base64.urlsafe_b64encode(sig).decode("ascii").rstrip("=")

    def _encode(self, payload: Dict[str, Any]) -> str:
        body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode(
            "utf-8"
        )
        body_b64 = base64.urlsafe_b64encode(body).decode("ascii").rstrip("=")
        sig = self._sign(body)
        return f"{body_b64}.{sig}"

    def _decode(self, token: str) -> Dict[str, Any]:
        try:
            body_b64, sig = token.split(".")
            body = base64.urlsafe_b64decode(body_b64 + "=")
            expected = self._sign(body)
            if not hmac.compare_digest(expected, sig):
                raise TokenError("invalid signature")
            payload = cast(Dict[str, Any], json.loads(body.decode("utf-8")))
            return payload
        except ValueError:
            raise TokenError("malformed token")

    def issue_token(self, subject: str, expires_in: int = 3600) -> str:
        now = int(time.time())
        payload = {"sub": subject, "iat": now, "exp": now + int(expires_in)}
        return self._encode(payload)

    def validate_token(self, token: str) -> Dict[str, Any]:
        payload = self._decode(token)
        now = int(time.time())
        if "exp" not in payload or "sub" not in payload:
            raise TokenError("invalid payload")
        if int(payload["exp"]) < now:
            raise TokenError("token expired")
        return payload

    def refresh_token(self, token: str, additional_lifetime: int = 3600) -> str:
        payload = self.validate_token(token)
        # Issue a new token with extended expiry
        return self.issue_token(payload["sub"], expires_in=additional_lifetime)
