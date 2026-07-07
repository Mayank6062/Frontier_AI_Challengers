from __future__ import annotations

from typing import Any
from datetime import timedelta, datetime

from .models import Session
from .session_repository import SessionRepository, SessionNotFoundError


class SessionValidationError(Exception):
    pass


class SessionManager:
    """Manages sessions lifecycle. Depends on SessionRepository via constructor injection."""

    def __init__(
        self, repository: SessionRepository, default_ttl_seconds: int = 3600
    ) -> None:
        self._repo = repository
        self._default_ttl = default_ttl_seconds

    def create_session(
        self,
        user_id: str,
        ttl_seconds: int | None = None,
        data: dict[str, Any] | None = None,
    ) -> Session:
        if not user_id or not user_id.strip():
            raise SessionValidationError("user_id required")
        ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
        s = Session(user_id=user_id, data=data or {})
        expiry = datetime.utcnow() + timedelta(seconds=ttl)
        s = Session.from_dict({**s.to_dict(), "expires_at": expiry.isoformat()})
        self._repo.save(s)
        return s

    def get_session(self, session_id: str) -> Session:
        try:
            s = self._repo.get(session_id)
        except SessionNotFoundError:
            raise
        if s.is_expired():
            self._repo.delete(session_id)
            raise SessionValidationError("session expired")
        return s

    def touch_session(self, session_id: str, ttl_seconds: int | None = None) -> Session:
        s = self.get_session(session_id)
        new = s.touch(ttl_seconds)
        self._repo.save(new)
        return new

    def list_sessions(self, user_id: str) -> list[Session]:
        """List all sessions for a specific user."""
        if not user_id or not user_id.strip():
            raise SessionValidationError("user_id required")
        # Filter out expired sessions and collect valid ones
        sessions = []
        for s in self._repo.list_by_user(user_id):
            if not s.is_expired():
                sessions.append(s)
            else:
                # Clean up expired sessions
                self._repo.delete(s.id)
        return sessions

    def invalidate(self, session_id: str) -> None:
        self._repo.delete(session_id)
