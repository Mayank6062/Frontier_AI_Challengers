"""
Hash Utils — Deterministic hashing and stable key generation.

Provides side-effect-free hashing functions for deterministic key generation.
Responsibility: Offer stable, reproducible hash operations.
"""

import hashlib
import json
from typing import Any, Dict


def compute_sha256(data: bytes) -> str:
    """
    Compute SHA-256 hash of bytes.

    Args:
        data: Bytes to hash.

    Returns:
        Hexadecimal hash string (64 characters).
    """
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    return hashlib.sha256(data).hexdigest()


def compute_text_hash(text: str) -> str:
    """
    Compute SHA-256 hash of text (UTF-8 encoded).

    Args:
        text: Text to hash.

    Returns:
        Hexadecimal hash string (64 characters).
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return compute_sha256(text.encode("utf-8"))


def compute_json_hash(obj: Any) -> str:
    """
    Compute SHA-256 hash of JSON-serializable object.

    Ensures deterministic hashing by using sorted keys and consistent formatting.

    Args:
        obj: JSON-serializable object.

    Returns:
        Hexadecimal hash string (64 characters).

    Raises:
        TypeError: If object is not JSON-serializable.
    """
    try:
        json_str = json.dumps(obj, sort_keys=True, separators=(",", ":"))
        return compute_text_hash(json_str)
    except (TypeError, ValueError) as e:
        raise TypeError(f"Object not JSON-serializable: {e}") from e


def compute_dict_hash(data: Dict[str, Any]) -> str:
    """
    Compute SHA-256 hash of dictionary.

    Ensures deterministic hashing by using sorted keys.

    Args:
        data: Dictionary to hash.

    Returns:
        Hexadecimal hash string (64 characters).

    Raises:
        TypeError: If dictionary is not JSON-serializable.
    """
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")
    return compute_json_hash(data)


def stable_key(*parts: Any) -> str:
    """
    Generate stable key from multiple parts.

    Useful for cache keys, ledger entry keys, etc.

    Args:
        *parts: Parts to combine into key.

    Returns:
        Stable key combining all parts.
    """
    if not parts:
        raise ValueError("Must provide at least one part")
    combined = "|".join(str(p) for p in parts)
    return compute_text_hash(combined)
