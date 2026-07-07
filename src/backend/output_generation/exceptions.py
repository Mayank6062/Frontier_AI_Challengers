"""Exception hierarchy for the Output Generation layer (Chapter 18).

All custom errors inherit from OutputGenerationError. Per CGR-06 all errors
are typed and include structured fields where appropriate.
"""

from __future__ import annotations

from typing import Optional


class OutputGenerationError(Exception):
    """Base exception for output generation domain errors."""

    def __init__(self, message: str, *, details: Optional[dict] = None) -> None:
        super().__init__(message)
        self.details = details or {}


class ValidationError(OutputGenerationError):
    """Raised when a validation step fails."""


class GenerationError(OutputGenerationError):
    """Raised when a generation pipeline stage fails irrecoverably."""


class StorageError(OutputGenerationError):
    """Raised on storage persistence or retrieval failures."""


class OrchestrationError(OutputGenerationError):
    """Raised when pipeline orchestration fails or invariant violated."""


class ConfigurationError(OutputGenerationError):
    """Raised when configuration or environment is invalid."""


__all__ = [
    "OutputGenerationError",
    "ValidationError",
    "GenerationError",
    "StorageError",
    "OrchestrationError",
    "ConfigurationError",
]
