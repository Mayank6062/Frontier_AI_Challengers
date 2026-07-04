"""Pytest fixtures for constants tests."""

import pytest


@pytest.fixture
def agent_constants():
    """Provide agent constants."""
    from ..agent_constants import (
        AGENT_STATE_PENDING,
        AGENT_STATE_RUNNING,
        AGENT_STATE_COMPLETED,
    )

    return {
        "PENDING": AGENT_STATE_PENDING,
        "RUNNING": AGENT_STATE_RUNNING,
        "COMPLETED": AGENT_STATE_COMPLETED,
    }
