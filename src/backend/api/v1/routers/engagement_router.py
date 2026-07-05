from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import cast

from ...schemas.engagement_schemas import (
    EngagementCreateRequest,
    EngagementResponse,
    EngagementUpdateRequest,
)
from ...dependencies.service_deps import DIContainer
from backend.core.engagement.engagement_repository import EngagementRepository
from backend.core.engagement.engagement_manager import (
    EngagementManager,
    ValidationError,
)
from backend.core.interfaces.storage_interface import StorageInterface

router = APIRouter()


def _eng_manager_provider(request: Request) -> EngagementManager:
    provided: DIContainer.Provided = request.app.state.di_provided
    repo = EngagementRepository(cast(StorageInterface, provided.engagement_store))
    return EngagementManager(repo)


@router.post(
    "/", response_model=EngagementResponse, status_code=status.HTTP_201_CREATED
)
def create_engagement(
    req: EngagementCreateRequest,
    manager: EngagementManager = Depends(_eng_manager_provider),
) -> EngagementResponse:
    try:
        e = manager.create(req.title, req.description)
        return EngagementResponse.from_orm(e)
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{eng_id}", response_model=EngagementResponse)
def get_engagement(
    eng_id: str, manager: EngagementManager = Depends(_eng_manager_provider)
) -> EngagementResponse:
    try:
        e = manager.get(eng_id)
        return EngagementResponse.from_orm(e)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/{eng_id}", response_model=EngagementResponse)
def update_engagement(
    eng_id: str,
    req: EngagementUpdateRequest,
    manager: EngagementManager = Depends(_eng_manager_provider),
) -> EngagementResponse:
    try:
        e = manager.update(eng_id, title=req.title, description=req.description)
        return EngagementResponse.from_orm(e)
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
