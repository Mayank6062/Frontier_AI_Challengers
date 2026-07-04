"""
Exceptions — Canonical shared exception hierarchy for platform error handling.

Provides structured, domain-agnostic exceptions consumed by all layers.
"""

from .base_exception import (
    AgentSharedError,
    ConfigurationError,
    DependencyError,
    SerializationError,
    SharedError,
    ValidationError,
)

__all__ = [
    "SharedError",
    "ValidationError",
    "SerializationError",
    "ConfigurationError",
    "DependencyError",
    "AgentSharedError",
]
