from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.time()
        response = await call_next(request)
        elapsed = (time.time() - start) * 1000.0
        logger = getattr(request.app.state, "di_provided", None)
        # If DI logger available, use it
        if logger and hasattr(logger, "logger"):
            try:
                logger.logger.emit_log("info", "request", {"path": request.url.path, "ms": elapsed})
            except Exception:
                pass
        return response
