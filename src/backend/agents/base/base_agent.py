from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional

from ...shared.models.types import Citation, TokenUsage, UUIDStr


class ExecutionStatus(str, Enum):
    SUCCESS = "SUCCESS"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class AgentContext:
    context_id: UUIDStr
    engagement_id: UUIDStr
    session_id: UUIDStr
    correlation_id: UUIDStr
    stage: str
    agent_id: str
    engagement_inputs: Dict[str, Any]
    structured_requirements: Optional[Dict[str, Any]] = None
    retrieved_knowledge: Optional[Dict[str, Any]] = None
    prior_stage_outputs: Optional[Mapping[str, "AgentResult"]] = None
    architect_overrides: Optional[List[Any]] = None
    refinement_feedback: Optional[str] = None
    agent_configuration: Optional[Dict[str, Any]] = None
    execution_version: int = 1
    domain_context: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class AgentResult:
    result_id: UUIDStr
    agent_id: str
    agent_version: str
    prompt_version: str
    model_id: str
    execution_status: ExecutionStatus
    output: Dict[str, Any]
    citations: List[Citation]
    confidence_score: float
    confidence_breakdown: Dict[str, float]
    tokens_consumed: TokenUsage
    execution_latency_ms: int
    retrieval_metadata: Optional[Dict[str, Any]] = None
    degradation_reason: Optional[str] = None
    failure_reason: Optional[Dict[str, Any]] = None
    context_id: Optional[UUIDStr] = None
    produced_at: Optional[str] = None
