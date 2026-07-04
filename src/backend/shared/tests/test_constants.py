"""Tests for shared constants to improve repo coverage."""

from backend.shared.constants import (
    agent_constants,
    engagement_states,
    platform_constants,
)


def test_agent_constants_values() -> None:
    assert isinstance(agent_constants.DEFAULT_AGENT_TIMEOUT_SECONDS, int)
    assert agent_constants.DEFAULT_AGENT_TIMEOUT_SECONDS > 0
    assert isinstance(agent_constants.DEFAULT_AGENT_RETRIES, int)


def test_engagement_state_constants() -> None:
    assert engagement_states.ENGAGEMENT_STATE_DRAFT == "draft"
    assert engagement_states.ENGAGEMENT_STATE_PUBLISHED == "published"


def test_platform_constants() -> None:
    assert platform_constants.DEFAULT_PAGE_SIZE == 50
    assert "%Y" in platform_constants.ISO_TIMESTAMP_FORMAT
