"""
Utils — General-purpose helper functions for shared use.

Provides text sanitization, hashing, retry primitives, timestamp helpers, and input sanitization.
"""

from .hash_utils import compute_dict_hash, compute_json_hash, compute_sha256, compute_text_hash, stable_key
from .retry_utils import BackoffStrategy, RetryConfig, retry_with_backoff
from .sanitizer import sanitize_identifier, sanitize_json_string, sanitize_prompt_input
from .text_utils import escape_markdown, pluralize, sanitize_text, truncate_text
from .time_utils import (
    current_iso_timestamp,
    current_utc_timestamp,
    format_iso_timestamp,
    parse_iso_timestamp,
    parse_unix_timestamp,
    to_unix_timestamp,
)

__all__ = [
    # text_utils
    "sanitize_text",
    "truncate_text",
    "escape_markdown",
    "pluralize",
    # hash_utils
    "compute_sha256",
    "compute_text_hash",
    "compute_json_hash",
    "compute_dict_hash",
    "stable_key",
    # retry_utils
    "RetryConfig",
    "BackoffStrategy",
    "retry_with_backoff",
    # time_utils
    "parse_iso_timestamp",
    "format_iso_timestamp",
    "current_utc_timestamp",
    "current_iso_timestamp",
    "parse_unix_timestamp",
    "to_unix_timestamp",
    # sanitizer
    "sanitize_prompt_input",
    "sanitize_json_string",
    "sanitize_identifier",
]
