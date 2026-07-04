"""
Decision Ledger Interface Contract.

Defines the immutable, append-only write contract for the Decision Ledger.
The Decision Ledger is the platform's audit trail and accountability mechanism.
Every significant event — every agent completion, every review decision, every
approval — is recorded here before the state transition is acknowledged.

Authority:
    BACKEND_MODULE_ARCHITECTURE.md Section 4.6 (interfaces module responsibilities)
    BACKEND_MODULE_ARCHITECTURE.md Section 4.13 (decision_ledger_service)
    BACKEND_MODULE_ARCHITECTURE.md Section 8 (LedgerRepository)
    SYSTEM_ARCHITECTURE.md Section 4.10 (Decision Ledger)

Implementors:
    src/backend/infrastructure/decision_ledger_service.py

Consumers:
    src/backend/core/engagement/ (every state transition)
    src/backend/core/review/ (every review decision)
    src/backend/agents/governance/human_collaboration/ (proposal recording)

Critical contract:
    append() is a durable write. The engagement state transition that triggered
    the append does NOT advance until append() returns successfully. A partial
    write must be retried — the append operation is idempotent when retried with
    the same entry_id.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Ledger entry models
# ---------------------------------------------------------------------------


class LedgerEventType(str, Enum):
    """
    Canonical event types recorded in the Decision Ledger.

    Each event type represents a specific, significant platform event.
    The event type determines the expected payload structure.
    """

    ENGAGEMENT_CREATED = "engagement.created"
    ENGAGEMENT_STATE_TRANSITION = "engagement.state_transition"
    AGENT_STAGE_COMPLETED = "agent.stage_completed"
    AGENT_STAGE_FAILED = "agent.stage_failed"
    PROPOSAL_SUBMITTED_FOR_REVIEW = "review.proposal_submitted"
    REVIEW_DECISION_APPROVED = "review.decision_approved"
    REVIEW_DECISION_REJECTED = "review.decision_rejected"
    REVIEW_DECISION_REFINEMENT = "review.decision_refinement"
    ARCHITECT_OVERRIDE_RECORDED = "review.override_recorded"
    ARCHITECTURE_APPROVED = "architecture.approved"
    ARCHITECTURE_FINALIZED = "architecture.finalized"
    OUTPUT_GENERATED = "output.generated"
    KNOWLEDGE_ENTRY_APPROVED = "knowledge.entry_approved"
    GOVERNANCE_VIOLATION_DETECTED = "governance.violation_detected"
    GOVERNANCE_CHECK_PASSED = "governance.check_passed"
    SESSION_CREATED = "session.created"
    SESSION_RESTORED = "session.restored"


@dataclass(frozen=True)
class LedgerEntry:
    """
    A single immutable record in the Decision Ledger.

    Once written, no field in a LedgerEntry is ever modified. The hash
    chain (prior_entry_hash → entry_hash) provides tamper evidence.

    Attributes:
        entry_id: Globally unique identifier for this ledger entry.
        event_type: The canonical event type that triggered this entry.
        engagement_id: The engagement this entry relates to. Empty string
            for platform-level events (e.g., session.created).
        session_id: The session this entry relates to.
        actor_id: The identity of the actor who triggered the event.
            Empty string for system-generated events.
        actor_type: "human" for architect-initiated events, "system" for
            automated events, "agent" for agent-generated events.
        payload: Event-specific data. Structure depends on event_type.
        occurred_at_utc: ISO 8601 UTC timestamp of the event occurrence.
        prior_entry_hash: SHA-256 hash of the immediately preceding ledger
            entry for this engagement. Empty string for the first entry.
        agent_id: The agent ID if this entry was triggered by an agent
            execution. Empty string for non-agent events.
        agent_version: The agent version at the time of this entry.
        prompt_version: The prompt version used by the agent, if applicable.
    """

    entry_id: str
    event_type: LedgerEventType
    engagement_id: str
    session_id: str
    actor_id: str
    actor_type: str
    payload: dict[str, Any]
    occurred_at_utc: str
    prior_entry_hash: str = ""
    agent_id: str = ""
    agent_version: str = ""
    prompt_version: str = ""


@dataclass(frozen=True)
class LedgerWriteResult:
    """
    Result of a durable ledger write.

    Attributes:
        entry_id: The entry ID that was written.
        entry_hash: SHA-256 hash of the written entry (for chain linking).
        written_at_utc: ISO 8601 UTC timestamp of the write confirmation.
        success: True when the write is durably confirmed.
    """

    entry_id: str
    entry_hash: str
    written_at_utc: str
    success: bool


@dataclass(frozen=True)
class LedgerIntegrityResult:
    """
    Result of a hash chain integrity verification.

    Attributes:
        valid: True if the chain is intact from the checked entry to the
            most recent entry.
        entries_verified: Number of entries verified in the check.
        first_broken_entry_id: The entry ID where the chain breaks.
            None if the chain is intact.
        verification_completed_at_utc: ISO 8601 UTC timestamp of verification.
    """

    valid: bool
    entries_verified: int
    first_broken_entry_id: str | None
    verification_completed_at_utc: str


# ---------------------------------------------------------------------------
# Interface contract
# ---------------------------------------------------------------------------


class LedgerInterface(ABC):
    """
    Abstract contract for the Decision Ledger adapter.

    The Decision Ledger is append-only. Once written, entries are never
    modified or deleted. The interface exposes append and read operations
    only — there are no update or delete methods.

    Contract invariants:
        - append() is durable: the caller must receive confirmation before
          the triggering state transition proceeds.
        - append() is idempotent: retrying with the same entry_id must not
          create a duplicate entry.
        - get() returns None for a non-existent entry_id.
        - list_by_engagement() returns entries in chronological order.
        - verify_chain() reads entries but never modifies them.

    Raises:
        LedgerWriteError: On append failure after retry exhaustion.
        LedgerReadError: On read failure after retry exhaustion.
        LedgerConnectionError: When the ledger backend is unavailable.
    """

    @abstractmethod
    async def append(self, entry: LedgerEntry) -> LedgerWriteResult:
        """
        Append an immutable entry to the Decision Ledger.

        This operation must complete durably before the method returns.
        The implementation must compute and store the chain hash before
        confirming the write.

        Args:
            entry: The complete ledger entry to append. Must have all
                required fields populated before calling.

        Returns:
            LedgerWriteResult: Confirmation with entry hash and timestamp.

        Raises:
            LedgerWriteError: On durable write failure after retry exhaustion.
        """

    @abstractmethod
    async def get(self, entry_id: str) -> LedgerEntry | None:
        """
        Retrieve a single ledger entry by its identifier.

        Args:
            entry_id: The globally unique entry identifier.

        Returns:
            LedgerEntry: The entry if found, None if not found.

        Raises:
            LedgerReadError: On storage backend failure.
        """

    @abstractmethod
    async def list_by_engagement(
        self,
        engagement_id: str,
        offset: int = 0,
        limit: int = 50,
    ) -> list[LedgerEntry]:
        """
        Retrieve a paginated list of ledger entries for an engagement.

        Results are returned in chronological order (oldest first).

        Args:
            engagement_id: The engagement to retrieve entries for.
            offset: Number of entries to skip (for pagination).
            limit: Maximum number of entries to return.

        Returns:
            list[LedgerEntry]: Chronologically ordered entries for the engagement.

        Raises:
            LedgerReadError: On storage backend failure.
        """

    @abstractmethod
    async def verify_chain(self, from_entry_id: str) -> LedgerIntegrityResult:
        """
        Verify the hash chain integrity from the given entry to the most recent.

        Used by scheduled integrity checks and audit queries. Does not modify
        any entries.

        Args:
            from_entry_id: The entry ID to start verification from.

        Returns:
            LedgerIntegrityResult: Verification outcome with details.

        Raises:
            LedgerReadError: On storage backend failure during verification.
        """

    @abstractmethod
    async def check_health(self) -> bool:
        """
        Check whether the ledger backend is currently operational.

        Must not raise on connectivity failure — must return False instead.

        Returns:
            bool: True if the ledger backend is reachable and operational.
        """
