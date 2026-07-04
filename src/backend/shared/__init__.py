"""
Shared Layer — Framework-level utilities, models, exceptions, and constants.

Provides cross-cutting, domain-agnostic utilities consumed by all backend layers.
Contains zero business logic and zero project module dependencies.

Public API:
    models: BaseModel, Identifier, Timestamp, PaginationParams, PaginatedResult
    exceptions: SharedError and derived exception hierarchy
    utils: text, hash, retry, time utilities and sanitization functions
    constants: agent, engagement, platform constants and operational limits
"""

from .constants import *
from .exceptions import *
from .models import *
from .utils import *

__all__ = [
    # Models
    "BaseModel",
    "Identifier",
    "Timestamp",
    "PaginationParams",
    "PaginatedResult",
    # Exceptions
    "SharedError",
    "ValidationError",
    "SerializationError",
    "ConfigurationError",
    "DependencyError",
    "AgentSharedError",
    # Utils (text)
    "sanitize_text",
    "truncate_text",
    "escape_markdown",
    "pluralize",
    # Utils (hash)
    "compute_sha256",
    "compute_text_hash",
    "compute_json_hash",
    "compute_dict_hash",
    "stable_key",
    # Utils (retry)
    "RetryConfig",
    "BackoffStrategy",
    "retry_with_backoff",
    # Utils (time)
    "parse_iso_timestamp",
    "format_iso_timestamp",
    "current_utc_timestamp",
    "current_iso_timestamp",
    "parse_unix_timestamp",
    "to_unix_timestamp",
    # Utils (sanitizer)
    "sanitize_prompt_input",
    "sanitize_json_string",
    "sanitize_identifier",
]
