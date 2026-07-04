"""
Pagination — Generic pagination descriptor.

Provides tooling-level pagination model for result sets.
Responsibility: Define canonical pagination parameters and results wrapper.
"""

from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class PaginationParams:
    """
    Immutable pagination parameters.

    Attributes:
        offset: Zero-based offset into result set.
        limit: Maximum number of items to return.
        cursor: Optional opaque cursor for keyset-based pagination.
    """

    offset: int = 0
    limit: int = 50

    def __post_init__(self) -> None:
        """Validate pagination parameters."""
        if self.offset < 0:
            raise ValueError("offset must be non-negative")
        if self.limit <= 0:
            raise ValueError("limit must be positive")


@dataclass(frozen=True)
class PaginatedResult(Generic[T]):
    """
    Generic paginated result wrapper.

    Attributes:
        items: List of result items.
        total_count: Total number of items available (may be approximate).
        offset: Offset of current result page.
        limit: Limit used for current result page.
        has_more: Whether more items are available.
    """

    items: List[T]
    total_count: int
    offset: int
    limit: int
    has_more: bool

    def __post_init__(self) -> None:
        """Validate result consistency."""
        if self.offset < 0:
            raise ValueError("offset must be non-negative")
        if self.limit <= 0:
            raise ValueError("limit must be positive")
        if self.total_count < 0:
            raise ValueError("total_count must be non-negative")
        if len(self.items) > self.limit:
            raise ValueError("items count exceeds limit")
        if self.offset + len(self.items) > self.total_count and not self.has_more:
            raise ValueError("inconsistent pagination: items exceed total_count")

    def is_empty(self) -> bool:
        """Check if result set is empty."""
        return len(self.items) == 0
