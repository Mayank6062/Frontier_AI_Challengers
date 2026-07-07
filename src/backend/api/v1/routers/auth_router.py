from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ...schemas.auth_schemas import TokenRequest, TokenResponse
from ...dependencies.auth_deps import get_token_manager
from backend.core.auth.token_manager import TokenManager

router = APIRouter()


class OAuthUrlResponse(BaseModel):
    url: str


class OAuthCallbackRequest(BaseModel):
    code: str


class Identity(BaseModel):
    id: str
    username: str
    email: str
    name: str


@router.get("/github/url", response_model=OAuthUrlResponse)
def get_oauth_url() -> OAuthUrlResponse:
    """
    Get GitHub OAuth URL for frontend redirect.
    This is a mock implementation for E2E testing.
    """
    # In production, this would construct a real GitHub OAuth URL
    # For testing, we return a mock callback URL
    oauth_url = (
        "http://localhost:5173/login?code=mock_auth_code_123"
    )
    return OAuthUrlResponse(url=oauth_url)


@router.post("/github/callback", response_model=TokenResponse)
def handle_oauth_callback(
    req: OAuthCallbackRequest,
    token_mgr: TokenManager = Depends(get_token_manager)
) -> TokenResponse:
    """
    Handle GitHub OAuth callback.
    This is a mock implementation for E2E testing.
    """
    try:
        # Mock user for testing
        mock_username = "test_user"
        token = token_mgr.issue_token(mock_username)
        return TokenResponse(access_token=token, token_type="bearer")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/me", response_model=Identity)
def get_current_identity() -> Identity:
    """
    Get current user identity.
    This is a mock implementation for E2E testing.
    """
    return Identity(
        id="mock_user_123",
        username="test_user",
        email="test@example.com",
        name="Test User",
    )


@router.post("/token", response_model=TokenResponse)
def issue_token(
    req: TokenRequest, token_mgr: TokenManager = Depends(get_token_manager)
) -> TokenResponse:
    try:
        token = token_mgr.issue_token(req.username)
        return TokenResponse(access_token=token, token_type="bearer")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
