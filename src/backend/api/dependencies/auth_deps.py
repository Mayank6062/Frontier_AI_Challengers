from __future__ import annotations

from fastapi import Request, HTTPException, status

from .service_deps import DIContainer
from backend.core.auth.token_manager import TokenManager


def get_token_manager(request: Request) -> TokenManager:
    provided: DIContainer.Provided = request.app.state.di_provided
    # Expect secret stored in secrets manager under key 'jwt_secret'
    secret = provided.secrets.get_secret("jwt_secret")
    if not secret:
        # For safety in production, require a secret be configured
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="jwt_secret not configured")
    return TokenManager(secret.encode("utf-8"))
"""
Authentication-related dependency providers.

This module exposes factory functions used by API layer to obtain auth
dependencies. It only wires services from `service_deps` and contains no
business logic.
"""
