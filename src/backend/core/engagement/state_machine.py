from __future__ import annotations

from typing import Dict, Set

from .models import EngagementState


class InvalidTransitionError(Exception):
    pass


class EngagementStateMachine:
    """Encapsulates allowed state transitions for Engagements.

    The machine is deterministic and validates transitions explicitly.
    """

    # Define allowed transitions
    _transitions: Dict[EngagementState, Set[EngagementState]] = {
        EngagementState.DRAFT: {EngagementState.DESIGN},
        EngagementState.DESIGN: {EngagementState.REVIEW, EngagementState.DRAFT},
        EngagementState.REVIEW: {EngagementState.PUBLISHED, EngagementState.DRAFT},
        EngagementState.PUBLISHED: {EngagementState.ARCHIVED},
        EngagementState.ARCHIVED: set(),
    }

    @classmethod
    def allowed_targets(cls, source: EngagementState) -> Set[EngagementState]:
        return cls._transitions.get(source, set())

    @classmethod
    def validate_transition(
        cls, source: EngagementState, target: EngagementState
    ) -> None:
        if target not in cls.allowed_targets(source):
            raise InvalidTransitionError(f"Invalid transition {source} -> {target}")
