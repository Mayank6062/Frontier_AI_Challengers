from __future__ import annotations

from fastapi import Request

from .service_deps import DIContainer
from backend.core.session.session_repository import SessionRepository
from backend.core.session.session_manager import SessionManager


def get_session_manager(request: Request) -> SessionManager:
    provided: DIContainer.Provided = request.app.state.di_provided
    repo = SessionRepository(provided.session_store)
    return SessionManager(repo)
"""Session-related dependency providers.

Exposes lightweight wiring for session management components. No business
logic is implemented here — only constructor-injection assembly.
"""
