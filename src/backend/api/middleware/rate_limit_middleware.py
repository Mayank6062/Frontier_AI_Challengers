from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import status
from fastapi.responses import JSONResponse
import time


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.calls = calls
        self.window = window_seconds

    async def dispatch(self, request: Request, call_next) -> Response:
        # Simple in-memory per-IP rate limiting using app.state; suitable for single-process.
        ip = request.client.host if request.client else "unknown"
        store = getattr(request.app.state, "rate_limit_store", None)
        if store is None:
            store = {}
            request.app.state.rate_limit_store = store
        now = int(time.time())
        bucket = store.get(ip, [])
        # purge old
        bucket = [t for t in bucket if now - t < self.window]
        if len(bucket) >= self.calls:
            return JSONResponse({"detail": "rate limit exceeded"}, status_code=status.HTTP_429_TOO_MANY_REQUESTS)
        bucket.append(now)
        store[ip] = bucket
        return await call_next(request)
