from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List


class AC_SCORE_01(BaseModel):
    id: str = Field(default="AC-SCORE-01")
    title: str = Field(default="Architecture Score: Input Completeness")
    description: str = Field(
        default="Ensure all required inputs for scoring are present and well-formed."
    )
    severity: str = Field(default="error")

    model_config = {"extra": "forbid", "frozen": True}


class AC_SCORE_02(BaseModel):
    id: str = Field(default="AC-SCORE-02")
    title: str = Field(default="Architecture Score: Evidence Linkage")
    description: str = Field(
        default="All claims must have at least one evidence citation where applicable."
    )
    severity: str = Field(default="warn")

    model_config = {"extra": "forbid", "frozen": True}


class AP_SCORE_01(BaseModel):
    id: str = Field(default="AP-SCORE-01")
    title: str = Field(default="Architecture Score: Approved Snapshot Present")
    description: str = Field(
        default="A signed/approved snapshot of the architecture must be attached when publishing scores."
    )
    severity: str = Field(default="error")

    model_config = {"extra": "forbid", "frozen": True}


class AP_SCORE_02(BaseModel):
    id: str = Field(default="AP-SCORE-02")
    title: str = Field(default="Architecture Score: Minimal Rationale")
    description: str = Field(
        default="Scores must include a concise rationale for any grade below B."
    )
    severity: str = Field(default="warn")

    model_config = {"extra": "forbid", "frozen": True}


class ValidationManifest(BaseModel):
    controls: List[str] = Field(default_factory=list)
    policies: List[str] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}
