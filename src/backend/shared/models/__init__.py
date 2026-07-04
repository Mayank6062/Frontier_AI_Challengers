"""
Models — Framework-level data types for shared use across all layers.

Provides BaseModel serialization contract, Identifier wrapper, Timestamp canonicalizer,
and generic Pagination descriptors.
"""

from .base_model import BaseModel
from .identifier import Identifier
from .pagination import PaginatedResult, PaginationParams
from .timestamp import Timestamp

__all__ = [
    "BaseModel",
    "Identifier",
    "Timestamp",
    "PaginationParams",
    "PaginatedResult",
]
