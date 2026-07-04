"""Pytest fixtures for exceptions tests."""

import pytest
from ..base_exception import SharedError


@pytest.fixture
def test_error():
    """Provide a test SharedError instance."""
    return SharedError("Test error", error_code="TEST", context={"key": "value"})
