from __future__ import annotations

import pytest
from backend.core.auth.token_manager import TokenManager, TokenError
from backend.core.auth.github_oauth import GitHubOAuth, OAuthError
from backend.core.auth.models import OAuthToken


def test_token_issue_and_validate() -> None:
    mgr = TokenManager(b"secret")
    tok = mgr.issue_token("user123", expires_in=2)
    payload = mgr.validate_token(tok)
    assert payload["sub"] == "user123"
    # create an already-expired token
    expired = mgr.issue_token("user123", expires_in=-1)
    with pytest.raises(TokenError):
        mgr.validate_token(expired)


def test_refresh() -> None:
    mgr = TokenManager(b"s")
    with pytest.raises(TokenError):
        mgr.refresh_token("invalid")


def test_github_oauth_url_and_exchange() -> None:
    gh = GitHubOAuth(client_id="cid")
    state = gh.generate_state()
    url = gh.authorization_url("https://app/cb", state)
    assert "client_id=cid" in url

    def fake_exchange(code: str) -> OAuthToken:
        if code != "ok":
            raise Exception("bad")
        return OAuthToken(
            access_token="a", token_type="bearer", scope=None, expires_in=3600
        )

    t = gh.exchange_code("ok", fake_exchange)
    assert t.access_token == "a"
    with pytest.raises(OAuthError):
        gh.exchange_code("", fake_exchange)
