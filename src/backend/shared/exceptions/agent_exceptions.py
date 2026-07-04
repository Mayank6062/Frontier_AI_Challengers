"""
Agent-specific exceptions extending SharedError.
"""
from __future__ import annotations

from .base_exception import SharedError


class AgentError(SharedError):
    """Base class for agent-related errors used by agents when raising through shared layer."""

