"""Unit tests for constants module."""

import pytest

from ..agent_constants import (
    AGENT_STATE_PENDING,
    AGENT_STATE_RUNNING,
    AGENT_STATE_COMPLETED,
    AGENT_STATE_FAILED,
    AGENT_STATE_DEGRADED,
    AGENT_STATUS_SUCCESS,
    DEFAULT_AGENT_TIMEOUT_SECONDS,
)
from ..engagement_constants import (
    ENGAGEMENT_STATE_CREATED,
    ENGAGEMENT_STATE_DISCOVERY,
    ENGAGEMENT_STATE_APPROVED,
    REVIEW_OUTCOME_APPROVED,
)
from ..platform_constants import (
    CORRELATION_ID_HEADER,
    DEFAULT_PAGE_SIZE,
    PLATFORM_NAME,
    API_VERSION,
)
from ..limits import (
    MAX_TEXT_INPUT_LENGTH,
    MAX_RETRY_ATTEMPTS,
    MIN_TIMEOUT_SECONDS,
)


class TestAgentConstants:
    """Tests for agent constants."""

    def test_agent_states_defined(self):
        """Test that agent states are defined."""
        assert AGENT_STATE_PENDING == "pending"
        assert AGENT_STATE_RUNNING == "running"
        assert AGENT_STATE_COMPLETED == "completed"
        assert AGENT_STATE_FAILED == "failed"
        assert AGENT_STATE_DEGRADED == "degraded"

    def test_agent_statuses_defined(self):
        """Test that agent statuses are defined."""
        assert AGENT_STATUS_SUCCESS == "success"

    def test_agent_timeouts_positive(self):
        """Test that timeouts are positive."""
        assert DEFAULT_AGENT_TIMEOUT_SECONDS > 0


class TestEngagementConstants:
    """Tests for engagement constants."""

    def test_engagement_states_defined(self):
        """Test that engagement states are defined."""
        assert ENGAGEMENT_STATE_CREATED == "created"
        assert ENGAGEMENT_STATE_DISCOVERY == "discovery"
        assert ENGAGEMENT_STATE_APPROVED == "approved"

    def test_review_outcomes_defined(self):
        """Test that review outcomes are defined."""
        assert REVIEW_OUTCOME_APPROVED == "approved"


class TestPlatformConstants:
    """Tests for platform constants."""

    def test_headers_defined(self):
        """Test that HTTP headers are defined."""
        assert CORRELATION_ID_HEADER == "X-Correlation-ID"

    def test_pagination_defaults(self):
        """Test pagination defaults."""
        assert DEFAULT_PAGE_SIZE > 0

    def test_platform_info_defined(self):
        """Test platform information."""
        assert PLATFORM_NAME == "ArchitectIQ"
        assert API_VERSION == "v1"


class TestLimits:
    """Tests for operational limits."""

    def test_text_limits_positive(self):
        """Test text limits are positive."""
        assert MAX_TEXT_INPUT_LENGTH > 0

    def test_retry_limits_positive(self):
        """Test retry limits are positive."""
        assert MAX_RETRY_ATTEMPTS > 0

    def test_timeout_limits_positive(self):
        """Test timeout limits are positive."""
        assert MIN_TIMEOUT_SECONDS > 0
