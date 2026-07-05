from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
def ping() -> dict[str, bool]:
    return {"ok": True}
