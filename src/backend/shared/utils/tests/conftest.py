"""Pytest fixtures for utils tests."""

import pytest
from ..retry_utils import RetryConfig, BackoffStrategy


@pytest.fixture
def retry_config():
    """Provide a test RetryConfig instance."""
    return RetryConfig(max_attempts=3, initial_delay_ms=10, jitter=False)


@pytest.fixture
def retry_config_exponential():
    """Provide an exponential RetryConfig."""
    return RetryConfig(
        max_attempts=3,
        initial_delay_ms=10,
        backoff_strategy=BackoffStrategy.EXPONENTIAL,
        jitter=False,
    )
