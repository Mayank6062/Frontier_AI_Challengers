from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable, Awaitable
from starlette.types import ASGIApp
from fastapi import status
from fastapi.responses import JSONResponse
import time


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, calls: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.calls = calls
        self.window = window_seconds

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Use DI-provided cache for rate limiting state so wiring remains in DI.
        ip = request.client.host if request.client else "unknown"
        provided = getattr(request.app.state, "di_provided", None)
        if provided is None:
            # If DI not available, fall back to in-memory (tests may set di_provided explicitly).
            store = getattr(request.app.state, "rate_limit_store", None)
            if store is None:
                store = {}
                request.app.state.rate_limit_store = store
            now = int(time.time())
            bucket = store.get(ip, [])
            bucket = [t for t in bucket if now - t < self.window]
            if len(bucket) >= self.calls:
                return JSONResponse(
                    {"detail": "rate limit exceeded"},
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                )
            bucket.append(now)
            store[ip] = bucket
            return await call_next(request)

        cache = getattr(provided, "cache", None)
        if cache is None:
            # Tests or lightweight stubs may not provide a cache; fall back to in-memory store.
            store = getattr(request.app.state, "rate_limit_store", None)
            if store is None:
                store = {}
                request.app.state.rate_limit_store = store
            now = int(time.time())
            bucket = store.get(ip, [])
            bucket = [t for t in bucket if now - t < self.window]
            if len(bucket) >= self.calls:
                return JSONResponse(
                    {"detail": "rate limit exceeded"},
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                )
            bucket.append(now)
            store[ip] = bucket
            return await call_next(request)
        key = f"ratelimit:{ip}"
        now = int(time.time())
        bucket = cache.get(key) or []
        # purge old
        bucket = [t for t in bucket if now - t < self.window]
        if len(bucket) >= self.calls:
            return JSONResponse(
                {"detail": "rate limit exceeded"},
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        bucket.append(now)
        # store updated bucket with TTL equal to the window
        cache.set(key, bucket, ttl_seconds=self.window)
        return await call_next(request)
