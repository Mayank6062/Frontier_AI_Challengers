from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class StageStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


@dataclass
class StageResult:
    stage_id: str
    status: StageStatus
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    confidence: Optional[float] = None
    citations: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass
class WorkflowContext:
    engagement_id: str
    input_payload: Dict[str, Any]
    accumulated: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionPlan:
    stage_groups: List[List[str]]  # list of stage_id groups (parallel groups)


@dataclass
class StageDefinition:
    stage_id: str
    agent_id: Optional[str] = None
    timeout_seconds: Optional[int] = None
    required: bool = True
