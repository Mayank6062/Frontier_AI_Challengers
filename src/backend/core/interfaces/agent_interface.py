"""
Agent Interface Contract.

Defines the base execution contract for all 12 specialized agents in the
platform. Every agent must implement this interface. The Orchestration Layer
dispatches to agents through this contract — it never has knowledge of any
specific agent's implementation.

The interface enforces the canonical 9-step agent execution lifecycle
(validate → retrieve → construct → sanitize → invoke → parse → validate →
cite → score → emit) through its method signatures. The concrete enforcement
of this lifecycle is provided by the BaseAgent abstract class in the agents
layer, which inherits this interface and implements the template method.

Authority:
    BACKEND_MODULE_ARCHITECTURE.md Section 4.6 (interfaces module responsibilities)
    BACKEND_MODULE_ARCHITECTURE.md Section 4.7 (base agent module)
    AI_AGENT_ARCHITECTURE.md Section 5 (contract-first)
    AI_AGENT_ARCHITECTURE.md Section 8 (BaseAgent template method)
    SYSTEM_ARCHITECTURE.md Section 4.7 (Agent Workers)

Implementors:
    src/backend/agents/base/base_agent.py (abstract base — enforces lifecycle)
    src/backend/agents/*/ (12 concrete agent implementations)

Consumers:
    src/backend/orchestration/agent_scheduler.py (dispatch via this interface)
    src/backend/orchestration/master_orchestrator.py (pipeline coordination)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Agent execution models (interface-local DTOs)
# ---------------------------------------------------------------------------


class AgentStatus(str, Enum):
    """
    Canonical agent execution status values.

    Authority: BACKEND_MODULE_ARCHITECTURE.md Section 4.7
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    DEGRADED = "degraded"


@dataclass(frozen=True)
class AgentCitation:
    """
    A traceable citation attached to an agent recommendation or finding.

    Every recommendation in an agent's output must have at least one citation.
    The AgentValidator rejects outputs where any recommendation lacks a citation.

    Attributes:
        knowledge_entry_id: The knowledge base entry that grounds this citation.
        entry_title: Human-readable title of the knowledge entry.
        source_reference: External source (standard, document, URL).
        relevance_score: How relevant this citation is to the recommendation.
    """

    knowledge_entry_id: str
    entry_title: str
    source_reference: str
    relevance_score: float


@dataclass(frozen=True)
class AgentContext:
    """
    The standardized input context provided to every agent at execution time.

    All agents receive an AgentContext. It contains everything the agent
    needs: the engagement state, the structured requirements, prior stage
    outputs, retrieved knowledge, and agent-specific configuration.

    Attributes:
        engagement_id: The engagement being processed.
        session_id: The session this engagement belongs to.
        correlation_id: Request correlation ID for distributed tracing.
        stage_name: The pipeline stage this agent is executing within.
        structured_requirements: The structured requirements from the
            Requirement Intelligence Agent output.
        prior_agent_outputs: Outputs from agents that ran before this agent
            in the pipeline. Keyed by agent_id.
        retrieved_knowledge: The context package from the Knowledge Retrieval
            Agent. Empty if this agent runs before knowledge retrieval.
        architect_feedback: Structured refinement feedback from the architect.
            Only present during targeted re-execution (refinement phase).
        model_id: The LLM model identifier to use for this execution.
        prompt_version: The prompt template version to load.
        agent_parameters: Agent-specific configuration parameters from
            the agent configuration file.
        max_tokens: Token budget for this agent's LLM invocation.
        temperature: Sampling temperature for this agent's LLM invocation.
        engagement_domain: The declared business domain of this engagement.
        compliance_frameworks: The regulatory frameworks declared for this
            engagement (e.g., ["gdpr", "soc2"]).
        metadata: Additional execution metadata.
    """

    engagement_id: str
    session_id: str
    correlation_id: str
    stage_name: str
    structured_requirements: dict[str, Any]
    prior_agent_outputs: dict[str, Any]
    retrieved_knowledge: dict[str, Any]
    architect_feedback: dict[str, Any]
    model_id: str
    prompt_version: str
    agent_parameters: dict[str, Any]
    max_tokens: int
    temperature: float
    engagement_domain: str
    compliance_frameworks: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentResult:
    """
    The standardized result emitted by every agent after execution.

    All agents return an AgentResult. The Orchestration Layer uses this
    model to aggregate results and route outputs to downstream agents.

    Attributes:
        agent_id: The AGENT_ID of the agent that produced this result.
        agent_version: The AGENT_VERSION at execution time.
        engagement_id: The engagement this result belongs to.
        correlation_id: Request correlation ID for tracing.
        status: The execution outcome status.
        output_payload: The agent's primary output data. Schema is
            agent-specific, defined by the agent's output model.
        citations: Citations attached to this result's recommendations.
            Must be non-empty for a COMPLETED result.
        confidence_score: Calculated confidence in this result (0.0–1.0).
        token_usage: Token consumption stats: {"input": int, "output": int}.
        latency_ms: End-to-end execution time in milliseconds.
        error_code: The error code if status is FAILED or DEGRADED.
        error_message: Human-readable error description.
        prompt_version: The prompt version used in this execution.
        metadata: Additional execution metadata for observability.
    """

    agent_id: str
    agent_version: str
    engagement_id: str
    correlation_id: str
    status: AgentStatus
    output_payload: dict[str, Any]
    citations: list[AgentCitation]
    confidence_score: float
    token_usage: dict[str, int]
    latency_ms: float
    error_code: str = ""
    error_message: str = ""
    prompt_version: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Interface contract
# ---------------------------------------------------------------------------


class AgentInterface(ABC):
    """
    Abstract contract for all 12 specialized agents.

    Defines the single public operation: execute(). The Orchestration Layer
    dispatches to agents exclusively through this interface. No orchestration
    code depends on any specific agent implementation.

    The complete 9-step agent execution lifecycle is enforced by the
    BaseAgent concrete abstract class in the agents layer, which extends
    this interface. The interface specifies the boundary; the base class
    specifies the lifecycle enforcement within that boundary.

    Contract invariants:
        - execute() must return an AgentResult for every outcome, including
          failures. It must never raise to the Orchestration Layer.
        - A COMPLETED result must have at least one citation.
        - A COMPLETED result must have a confidence_score between 0.0 and 1.0.
        - A FAILED result must have a non-empty error_code.
        - get_agent_id() must return a stable, unique AGENT_ID constant.
        - get_agent_version() must return the current semantic version.
        - is_async() must return True if execute() performs async operations.

    Raises:
        Nothing — all exceptions are caught and returned as FAILED AgentResults.
    """

    @abstractmethod
    async def execute(self, context: AgentContext) -> AgentResult:
        """
        Execute this agent with the provided context.

        The implementation must:
            1. Validate inputs against the agent's declared input schema.
            2. Retrieve relevant knowledge (if this agent uses the knowledge base).
            3. Construct the prompt from the versioned template and inputs.
            4. Sanitize the prompt (PII and injection detection).
            5. Invoke the LLM through the LLM interface.
            6. Parse and validate the LLM output against the output schema.
            7. Attach citations to every recommendation in the output.
            8. Calculate the confidence score.
            9. Emit the structured AgentResult.

        Must never raise to the caller. All exceptions are caught and
        returned as AgentResult with status=FAILED.

        Args:
            context: The standardized execution context containing all
                inputs this agent needs.

        Returns:
            AgentResult: The execution outcome. Always returned, never raised.
        """

    @abstractmethod
    def get_agent_id(self) -> str:
        """
        Return this agent's stable unique identifier.

        Must be a constant string defined as AGENT_ID on the class.
        Used by the AgentRegistry and AgentFactory for discovery and routing.

        Returns:
            str: The agent's unique identifier (e.g., "requirement_intelligence").
        """

    @abstractmethod
    def get_agent_version(self) -> str:
        """
        Return this agent's current semantic version.

        Must be a constant string defined as AGENT_VERSION on the class.
        Recorded in every AgentResult for audit and prompt version tracking.

        Returns:
            str: The agent version in semantic version format (e.g., "1.0.0").
        """

    @abstractmethod
    def get_agent_category(self) -> str:
        """
        Return this agent's pipeline category.

        Must be a constant defined as AGENT_CATEGORY on the class.
        Used by the Orchestrator to determine pipeline stage placement.

        Valid values: "discovery", "design", "validation", "governance".

        Returns:
            str: The agent's pipeline category.
        """

    @abstractmethod
    def get_input_schema(self) -> dict[str, Any]:
        """
        Return the JSON Schema for this agent's expected input.

        Used by the BaseAgent to validate AgentContext.structured_requirements
        and AgentContext.prior_agent_outputs before execute() proceeds.

        Returns:
            dict[str, Any]: JSON Schema describing the expected input structure.
        """

    @abstractmethod
    def get_output_schema(self) -> dict[str, Any]:
        """
        Return the JSON Schema for this agent's output payload.

        Used by the AgentValidator to validate the output_payload in the
        AgentResult before it is emitted to the Orchestration Layer.

        Returns:
            dict[str, Any]: JSON Schema describing the expected output structure.
        """
