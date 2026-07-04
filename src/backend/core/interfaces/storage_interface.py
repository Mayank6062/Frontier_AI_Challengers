"""
Storage Interface Contract.

Defines the normalized abstraction for all persistent structured storage
adapters. Application modules never issue raw storage queries — all
persistence operations pass through this interface. The storage implementation
is a deployment decision; the application layer never knows which storage
technology is in use.

Authority:
    BACKEND_MODULE_ARCHITECTURE.md Section 4.6 (interfaces module responsibilities)
    BACKEND_MODULE_ARCHITECTURE.md Section 7.3 (StorageProvider contract)

Implementors:
    src/backend/infrastructure/storage_service.py

Consumers:
    src/backend/core/ (session, engagement, auth, review modules via repositories)
    src/backend/infrastructure/ (decision_ledger_service via StorageInterface)
    src/backend/knowledge/ (knowledge_base module)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Query / Result models (interface-local DTOs)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StorageRecord:
    """
    A single persisted record returned from the storage layer.

    Attributes:
        key: The unique record identifier within its collection.
        collection: The collection (table/namespace) this record belongs to.
        data: The record's data payload as a dictionary.
        version: Optimistic-lock version for conflict detection.
            Incremented by the storage layer on every write.
        created_at_utc: ISO 8601 UTC timestamp of first write.
        updated_at_utc: ISO 8601 UTC timestamp of most recent write.
    """

    key: str
    collection: str
    data: dict[str, Any]
    version: int = 1
    created_at_utc: str = ""
    updated_at_utc: str = ""


@dataclass(frozen=True)
class StorageFilter:
    """
    Domain-expressed query predicate for storage reads.

    Deliberately simple: equality checks and limit/offset pagination.
    Complex joins and aggregations are not supported through this interface
    — they indicate a data model problem, not a missing interface capability.

    Attributes:
        collection: The collection to query.
        predicates: Key-value equality predicates. All predicates are ANDed.
        order_by: Optional field name to order results by.
        ascending: Whether to sort ascending. Defaults to True.
        limit: Maximum number of records to return. None means no limit.
        offset: Number of records to skip for pagination.
    """

    collection: str
    predicates: dict[str, Any] = field(default_factory=dict)
    order_by: str | None = None
    ascending: bool = True
    limit: int | None = None
    offset: int = 0


@dataclass(frozen=True)
class StorageWriteConfirmation:
    """
    Confirmation of a durable write operation.

    Attributes:
        key: The record key that was written.
        collection: The collection the record was written to.
        version: The version assigned to this write.
        written_at_utc: ISO 8601 UTC timestamp of the write.
        success: True if the write was confirmed durable.
    """

    key: str
    collection: str
    version: int
    written_at_utc: str
    success: bool


# ---------------------------------------------------------------------------
# Interface contract
# ---------------------------------------------------------------------------


class StorageInterface(ABC):
    """
    Abstract contract for all persistent structured storage adapters.

    All application code that needs to persist domain entities uses this
    interface. The interface exposes a minimal, domain-neutral API: read a
    record, write a record, delete a record, and query a collection.

    Contract invariants:
        - read() returns None for a non-existent key rather than raising.
        - write() must confirm durability before returning (write-ahead).
        - delete() is idempotent — deleting a non-existent key succeeds.
        - query() returns an empty list when no records match.
        - All writes are atomic per-record.

    Raises:
        StorageWriteError: On write failure after retry exhaustion.
        StorageReadError: On read failure after retry exhaustion.
        StorageConnectionError: When the storage backend is unavailable.
    """

    @abstractmethod
    async def read(self, collection: str, key: str) -> StorageRecord | None:
        """
        Read a single record by its key from the specified collection.

        Args:
            collection: The collection (table/namespace) to read from.
            key: The unique record identifier within the collection.

        Returns:
            StorageRecord: The record if found, None if not found.

        Raises:
            StorageReadError: On storage backend failure.
        """

    @abstractmethod
    async def write(
        self, collection: str, key: str, data: dict[str, Any]
    ) -> StorageWriteConfirmation:
        """
        Write (create or overwrite) a record with the given key.

        The write is confirmed durable before this method returns.
        Callers must not assume the write is durable until they receive
        a StorageWriteConfirmation with success=True.

        Args:
            collection: The collection (table/namespace) to write to.
            key: The unique record identifier within the collection.
            data: The record data payload.

        Returns:
            StorageWriteConfirmation: Write confirmation with version and timestamp.

        Raises:
            StorageWriteError: On write failure after retry exhaustion.
        """

    @abstractmethod
    async def delete(self, collection: str, key: str) -> StorageWriteConfirmation:
        """
        Delete the record identified by key from the collection.

        Idempotent: succeeds if the record does not exist.

        Args:
            collection: The collection (table/namespace) to delete from.
            key: The unique record identifier within the collection.

        Returns:
            StorageWriteConfirmation: Deletion confirmation.

        Raises:
            StorageWriteError: On storage backend failure.
        """

    @abstractmethod
    async def query(self, filter_spec: StorageFilter) -> list[StorageRecord]:
        """
        Query a collection using a structured domain filter.

        Args:
            filter_spec: The query specification with collection, predicates,
                ordering, and pagination parameters.

        Returns:
            list[StorageRecord]: List of matching records. Empty list if none match.

        Raises:
            StorageReadError: On storage backend failure.
        """

    @abstractmethod
    async def count(self, collection: str, predicates: dict[str, Any]) -> int:
        """
        Count records in a collection matching the given predicates.

        Args:
            collection: The collection to count in.
            predicates: Key-value equality predicates. All predicates are ANDed.

        Returns:
            int: The count of matching records.

        Raises:
            StorageReadError: On storage backend failure.
        """

    @abstractmethod
    async def check_health(self) -> bool:
        """
        Check whether the storage backend is currently operational.

        Must not raise on connectivity failure — must return False instead.
        Used by application health check endpoints.

        Returns:
            bool: True if the storage backend is reachable and operational.
        """
