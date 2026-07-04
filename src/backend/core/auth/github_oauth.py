from __future__ import annotations

from typing import Callable, Optional
from urllib.parse import urlencode
import secrets

from .models import OAuthToken


class OAuthError(Exception):
    pass


class GitHubOAuth:
    """Domain logic for GitHub OAuth flows.

    Note: network-bound token exchange is delegated to an injected callable
    to keep domain logic testable and infrastructure-agnostic.
    """

    AUTH_ENDPOINT = "https://github.com/login/oauth/authorize"

    def __init__(self, client_id: str, default_scope: str = "read:user") -> None:
        if not client_id:
            raise ValueError("client_id required")
        self._client_id = client_id
        self._default_scope = default_scope

    def generate_state(self) -> str:
        return secrets.token_urlsafe(16)

    def authorization_url(
        self, redirect_uri: str, state: str, scope: Optional[str] = None
    ) -> str:
        if not redirect_uri:
            raise OAuthError("redirect_uri required")
        params = {
            "client_id": self._client_id,
            "redirect_uri": redirect_uri,
            "state": state,
            "scope": scope or self._default_scope,
        }
        return f"{self.AUTH_ENDPOINT}?" + urlencode(params)

    def exchange_code(
        self, code: str, token_exchange_fn: Callable[[str], OAuthToken]
    ) -> OAuthToken:
        """Exchange the authorization code for an OAuthToken using provided callable.

        The callable must perform network IO and return a validated `OAuthToken`.
        """
        if not code:
            raise OAuthError("code required")
        if not callable(token_exchange_fn):
            raise OAuthError("token_exchange_fn must be callable")
        token = token_exchange_fn(code)
        if not isinstance(token, OAuthToken):
            raise OAuthError("invalid token response")
        return token
