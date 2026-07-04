from __future__ import annotations

from typing import Iterable

from .models import Engagement, EngagementState
from .state_machine import EngagementStateMachine, InvalidTransitionError
from backend.shared.models.timestamps import now_iso
from .engagement_repository import EngagementRepository, EngagementNotFoundError


class ValidationError(Exception):
    pass


class EngagementManager:
    """High-level use-case service for managing Engagement lifecycles.

    All dependencies are injected via constructor. Methods validate inputs
    and raise domain-specific exceptions on error.
    """

    def __init__(self, repository: EngagementRepository) -> None:
        self._repo = repository

    def create(self, title: str, description: str | None = None) -> Engagement:
        if not title or not title.strip():
            raise ValidationError("title is required")
        eng = Engagement(title=title.strip(), description=description)
        self._repo.save(eng)
        return eng

    def get(self, engagement_id: str) -> Engagement:
        try:
            return self._repo.get(engagement_id)
        except EngagementNotFoundError as exc:
            raise exc

    def list(self) -> Iterable[Engagement]:
        return self._repo.list()

    def transition(
        self, engagement_id: str, target_state: EngagementState
    ) -> Engagement:
        eng = self.get(engagement_id)
        try:
            EngagementStateMachine.validate_transition(eng.state, target_state)
        except InvalidTransitionError:
            raise
        new_eng = eng.with_state(target_state)
        self._repo.save(new_eng)
        return new_eng

    def update(
        self,
        engagement_id: str,
        *,
        title: str | None = None,
        description: str | None = None,
    ) -> Engagement:
        eng = self.get(engagement_id)
        data = eng.to_dict()
        if title is not None:
            if not title.strip():
                raise ValidationError("title cannot be empty")
            data["title"] = title.strip()
        if description is not None:
            data["description"] = description
        data["updated_at"] = now_iso()
        updated = Engagement.from_dict(data)
        self._repo.save(updated)
        return updated

    def delete(self, engagement_id: str) -> None:
        self._repo.delete(engagement_id)
