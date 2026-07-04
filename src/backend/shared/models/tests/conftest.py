"""Pytest fixtures for models tests."""

import pytest
from datetime import datetime, timezone


@pytest.fixture
def utc_datetime():
    """Provide a fixed UTC datetime for testing."""
    return datetime(2026, 7, 4, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def sample_uuid():
    """Provide a valid UUID for testing."""
    return "550e8400-e29b-41d4-a716-446655440000"
