from __future__ import annotations

from typing import Dict, Optional
from pydantic import BaseModel, Field


class DeterminismConfig(BaseModel):
    seed: Optional[int] = None
    deterministic_templates: bool = True

    model_config = {"extra": "forbid"}


class GenerationConfig(BaseModel):
    max_tokens: Optional[int] = None
    temperature: float = 0.0
    top_p: float = 1.0

    model_config = {"extra": "forbid"}


class VersionConfig(BaseModel):
    api_version: str = "v1"
    implementation_version: str = "0.1.0"

    model_config = {"extra": "forbid"}


class OutputSettings(BaseModel):
    feature_flags: Dict[str, bool] = Field(default_factory=dict)
    portal_thresholds: Dict[str, int] = Field(default_factory=dict)
    version: VersionConfig = Field(default_factory=VersionConfig)
    generation: GenerationConfig = Field(default_factory=GenerationConfig)
    determinism: DeterminismConfig = Field(default_factory=DeterminismConfig)

    model_config = {"extra": "forbid"}
