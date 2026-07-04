"""
Base Exception — Canonical shared exception hierarchy.

Provides domain-agnostic exception types for platform-wide error handling.
Responsibility: Define structured exception contract for all layers.
"""

from typing import Any, Dict, Optional


class SharedError(Exception):
    """
    Base exception for all platform errors.

    Provides structured error context including message, error code, and optional metadata.
    """

    error_code: str = "SHARED_ERROR"

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize SharedError.

        Args:
            message: Human-readable error message.
            error_code: Optional error code for programmatic handling.
            context: Optional metadata dict for debugging.
        """
        self.message = message
        self.error_code = error_code or self.error_code
        self.context = context or {}
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize error to dictionary.

        Returns:
            Dictionary representation of error.
        """
        return {
            "error_code": self.error_code,
            "message": self.message,
            "context": self.context,
        }

    def __repr__(self) -> str:
        """Representation."""
        return f"{self.__class__.__name__}({self.error_code}: {self.message})"


class ValidationError(SharedError):
    """Raised when validation fails."""

    error_code = "VALIDATION_ERROR"


class SerializationError(SharedError):
    """Raised when serialization/deserialization fails."""

    error_code = "SERIALIZATION_ERROR"


class ConfigurationError(SharedError):
    """Raised when configuration is invalid."""

    error_code = "CONFIGURATION_ERROR"


class DependencyError(SharedError):
    """Raised when a required dependency is missing or invalid."""

    error_code = "DEPENDENCY_ERROR"


class AgentSharedError(SharedError):
    """
    Adapter exception for agent-surface errors.

    Used to wrap agent-level errors into the platform error hierarchy.
    """

    error_code = "AGENT_ERROR"
