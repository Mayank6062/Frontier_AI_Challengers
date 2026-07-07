"""Integrity hasher utilities for manifest layer."""

from __future__ import annotations

import hashlib
import json
from typing import List, Dict


def compute_content_hash(file_bytes: bytes) -> str:
    """Compute SHA-256 hex digest for given bytes."""
    return hashlib.sha256(file_bytes).hexdigest()


def compute_composite_hash(manifest_files: List[Dict]) -> str:
    """
    Deterministic composite hash.
    Sort file hashes by relative_path (canonical key) before hashing.
    Expects manifest_files: list of dicts with keys (relative_path, content_hash)
    """
    sorted_hashes = sorted(
        [(f["relative_path"], f["content_hash"]) for f in manifest_files], key=lambda x: x[0]
    )
    composite_input = json.dumps(sorted_hashes, separators=(",", ":"))
    return hashlib.sha256(composite_input.encode("utf-8")).hexdigest()


__all__ = ["compute_content_hash", "compute_composite_hash"]
