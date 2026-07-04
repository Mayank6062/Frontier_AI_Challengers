from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status, Request

from ...schemas.session_schemas import SessionCreateRequest, SessionResponse
from ...dependencies.session_deps import get_session_manager
from backend.core.session.session_manager import SessionValidationError

router = APIRouter()


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(req: SessionCreateRequest, mgr=Depends(get_session_manager)) -> SessionResponse:
    try:
        s = mgr.create_session(req.user_id, ttl_seconds=req.ttl_seconds, data=req.data)
        return SessionResponse.from_orm(s)
    except SessionValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: str, mgr=Depends(get_session_manager)) -> SessionResponse:
    try:
        s = mgr.get_session(session_id)
        return SessionResponse.from_orm(s)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
