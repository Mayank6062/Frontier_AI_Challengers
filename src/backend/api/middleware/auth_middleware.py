from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable, Awaitable
from fastapi import status
from fastapi.responses import JSONResponse


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Extract Authorization header and attach token payload to request.state
        auth = request.headers.get("Authorization")
        if auth and auth.lower().startswith("bearer "):
            token = auth.split(" ", 1)[1]
            try:
                # Token validation delegated to TokenManager via dependency providers in routes
                # Middleware avoids business logic; it only checks header presence here
                request.state.token = token
            except Exception:
                return JSONResponse(
                    {"detail": "invalid token"},
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
        return await call_next(request)
