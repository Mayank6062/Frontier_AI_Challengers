"""Unit tests for exceptions module."""

import pytest

from ..base_exception import (
    SharedError,
    ValidationError,
    SerializationError,
    ConfigurationError,
    DependencyError,
    AgentSharedError,
)


class TestSharedError:
    """Tests for SharedError base exception."""

    def test_basic_error(self):
        """Test basic error construction."""
        error = SharedError("Test message")
        assert error.message == "Test message"
        assert error.error_code == "SHARED_ERROR"
        assert error.context == {}

    def test_error_with_code(self):
        """Test error with custom code."""
        error = SharedError("Test message", error_code="CUSTOM_CODE")
        assert error.error_code == "CUSTOM_CODE"

    def test_error_with_context(self):
        """Test error with context metadata."""
        context = {"key": "value", "count": 42}
        error = SharedError("Test message", context=context)
        assert error.context == context

    def test_to_dict(self):
        """Test serialization to dict."""
        error = SharedError("Test message", error_code="TEST", context={"key": "value"})
        result = error.to_dict()
        assert result["message"] == "Test message"
        assert result["error_code"] == "TEST"
        assert result["context"] == {"key": "value"}

    def test_repr(self):
        """Test string representation."""
        error = SharedError("Test message", error_code="TEST")
        repr_str = repr(error)
        assert "SharedError" in repr_str
        assert "TEST" in repr_str
        assert "Test message" in repr_str

    def test_is_exception(self):
        """Test that SharedError is an Exception."""
        error = SharedError("Test")
        assert isinstance(error, Exception)


class TestValidationError:
    """Tests for ValidationError."""

    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError("Invalid input")
        assert error.error_code == "VALIDATION_ERROR"

    def test_inheritance(self):
        """Test inheritance from SharedError."""
        error = ValidationError("Invalid input")
        assert isinstance(error, SharedError)


class TestSerializationError:
    """Tests for SerializationError."""

    def test_serialization_error(self):
        """Test SerializationError."""
        error = SerializationError("Failed to serialize")
        assert error.error_code == "SERIALIZATION_ERROR"


class TestConfigurationError:
    """Tests for ConfigurationError."""

    def test_configuration_error(self):
        """Test ConfigurationError."""
        error = ConfigurationError("Invalid config")
        assert error.error_code == "CONFIGURATION_ERROR"


class TestDependencyError:
    """Tests for DependencyError."""

    def test_dependency_error(self):
        """Test DependencyError."""
        error = DependencyError("Missing dependency")
        assert error.error_code == "DEPENDENCY_ERROR"


class TestAgentSharedError:
    """Tests for AgentSharedError."""

    def test_agent_error(self):
        """Test AgentSharedError."""
        error = AgentSharedError("Agent failed")
        assert error.error_code == "AGENT_ERROR"
