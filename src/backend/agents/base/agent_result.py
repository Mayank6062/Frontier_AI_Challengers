from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    success: bool
    status: str
    payload: Optional[Dict[str, Any]] = None
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    confidence: Optional[float] = None
    citations: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    execution_time_ms: Optional[float] = None
    agent_name: Optional[str] = None
    trace_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        frozen = True

    @classmethod
    def success_result(
        cls,
        payload: Optional[Dict[str, Any]] = None,
        confidence: Optional[float] = None,
        **kwargs: Any,
    ) -> "AgentResult":
        return cls(
            success=True,
            status="SUCCESS",
            payload=payload or {},
            confidence=confidence,
            **kwargs,
        )

    @classmethod
    def failure_result(cls, errors: List[str], **kwargs: Any) -> "AgentResult":
        return cls(success=False, status="FAILURE", errors=errors, payload={}, **kwargs)

    @classmethod
    def validation_error(cls, errors: List[str], **kwargs: Any) -> "AgentResult":
        return cls(
            success=False,
            status="VALIDATION_ERROR",
            errors=errors,
            payload={},
            **kwargs,
        )

    @classmethod
    def internal_error(cls, message: str, **kwargs: Any) -> "AgentResult":
        return cls(
            success=False,
            status="INTERNAL_ERROR",
            errors=[message],
            payload={},
            **kwargs,
        )
