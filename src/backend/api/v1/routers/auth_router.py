from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from ...schemas.auth_schemas import TokenRequest, TokenResponse
from ...dependencies.auth_deps import get_token_manager
from backend.core.auth.token_manager import TokenManager

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
def issue_token(
    req: TokenRequest, token_mgr: TokenManager = Depends(get_token_manager)
) -> TokenResponse:
    try:
        token = token_mgr.issue_token(req.username)
        return TokenResponse(access_token=token, token_type="bearer")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
