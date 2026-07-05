from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Centralized error translation for unknown exceptions
    return JSONResponse(
        {"detail": "internal server error", "error": str(exc)},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
