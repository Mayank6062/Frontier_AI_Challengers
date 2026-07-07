from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from .dependencies import service_deps
from .v1.routers import (
    auth_router,
    session_router,
    engagement_router,
    chat_router,
    workspace_router,
    output_router,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Frontier AI Gateway",
        description="API Gateway for Frontier AI services",
        version="1.0.0",
        openapi_url="/openapi.json",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(session_router.router, prefix="/api/v1/sessions", tags=["sessions"])
    app.include_router(
        engagement_router.router, prefix="/api/v1/engagements", tags=["engagements"]
    )
    app.include_router(chat_router.router, prefix="/api/v1/chat", tags=["chat"])
    app.include_router(
        workspace_router.router, prefix="/api/v1/workspace", tags=["workspace"]
    )
    app.include_router(output_router.router, prefix="/api/v1/output", tags=["output"])

    # Register middleware and exception handlers from package
    from .middleware import (
        auth_middleware,
        correlation_id_middleware,
        logging_middleware,
        error_handler_middleware,
        rate_limit_middleware,
    )

    app.add_middleware(correlation_id_middleware.CorrelationIDMiddleware)
    app.add_middleware(logging_middleware.RequestLoggingMiddleware)
    app.add_middleware(auth_middleware.AuthenticationMiddleware)
    app.add_middleware(rate_limit_middleware.RateLimitMiddleware)

    from starlette.requests import Request

    @app.exception_handler(Exception)
    async def _global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return await error_handler_middleware.global_exception_handler(request, exc)

    @app.on_event("startup")
    async def _startup_event() -> None:
        # Build DI container once and attach to app.state for dependency providers
        # For E2E testing, initialize with a default JWT secret
        default_secrets = {
            "jwt_secret": "dev-secret-key-for-e2e-testing"  # ONLY for testing, not for production
        }
        di = service_deps.DIContainer(secrets_initial=default_secrets)
        app.state.di_provided = di.build()

    @app.on_event("shutdown")
    async def _shutdown_event() -> None:
        # Graceful shutdown hooks (no business logic required here)
        pass

    @app.get("/healthz")
    async def _health() -> JSONResponse:
        return JSONResponse({"status": "ok"})

    @app.get("/version")
    async def _version() -> JSONResponse:
        return JSONResponse({"version": "1.0.0"})

    return app


app = create_app()
