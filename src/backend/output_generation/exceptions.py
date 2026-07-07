"""Exception hierarchy for the Output Generation layer (Chapter 18).

All custom errors inherit from OutputGenerationError. Per CGR-06 all errors
are typed and include structured fields where appropriate.
"""

from __future__ import annotations

from typing import Optional


class OutputGenerationError(Exception):
    """Base error for output generation failures.

    Attributes:
        message: Human readable message.
        code: Optional machine-readable code.
        details: Optional structured details.
    """

    def __init__(self, message: str, code: Optional[str] = None, details: Optional[dict] = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class ValidationError(OutputGenerationError):
    """Raised when input or intermediate validation fails (BLOCKER)."""


class GenerationError(OutputGenerationError):
    """Raised when a generator fails to produce output."""


class StorageError(OutputGenerationError):
    """Raised for storage backend failures (write/read/list)."""


class OrchestrationError(OutputGenerationError):
    """Raised when pipeline orchestration fails or invariant violated."""


__all__ = [
    "OutputGenerationError",
    "ValidationError",
    "GenerationError",
    "StorageError",
    "OrchestrationError",
]
from __future__ import annotations

from typing import Optional


class OutputGenerationError(Exception):
    """Base exception for output generation domain errors."""

    def __init__(self, message: str, *, details: Optional[dict] = None) -> None:
        super().__init__(message)
        self.details = details or {}


class ValidationError(OutputGenerationError):
    """Raised when a validation step fails."""


class StorageError(OutputGenerationError):
    """Raised on storage persistence or retrieval failures."""


class GenerationError(OutputGenerationError):
    """Raised when a generation pipeline stage fails irrecoverably."""


class ConfigurationError(OutputGenerationError):
    """Raised when configuration or environment is invalid."""


__all__ = [
    "OutputGenerationError",
    "ValidationError",
    "StorageError",
    "GenerationError",
    "ConfigurationError",
]
