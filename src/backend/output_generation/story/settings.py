from __future__ import annotations

from typing import Dict, Optional
from pydantic import BaseModel, Field


class NarrativeLimits(BaseModel):
    max_sections: int = 20
    max_characters: int = 20000

    model_config = {"extra": "forbid", "frozen": True}


class WordCountLimits(BaseModel):
    min_words: int = 50
    max_words: int = 2000

    model_config = {"extra": "forbid", "frozen": True}


class RetryPolicyConfiguration(BaseModel):
    max_retries: int = 0
    backoff_seconds: int = 0

    model_config = {"extra": "forbid", "frozen": True}


class TimeoutConfiguration(BaseModel):
    generation_timeout_seconds: int = 60

    model_config = {"extra": "forbid", "frozen": True}


class PersonaDefaults(BaseModel):
    default_persona: Optional[str] = None
    persona_visibility: Dict[str, bool] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class PromptVersion(BaseModel):
    version: str = "v1"

    model_config = {"extra": "forbid", "frozen": True}


class QualityThresholds(BaseModel):
    readability: float = 0.0
    confidence: float = 0.0

    model_config = {"extra": "forbid", "frozen": True}


class ReadabilityThresholds(BaseModel):
    flesch_kincaid: Optional[float] = None

    model_config = {"extra": "forbid", "frozen": True}


class ValidationSettings(BaseModel):
    enabled: bool = True
    thresholds: QualityThresholds = Field(default_factory=QualityThresholds)

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeSettings(BaseModel):
    limits: NarrativeLimits = Field(default_factory=NarrativeLimits)
    word_count: WordCountLimits = Field(default_factory=WordCountLimits)
    retry: RetryPolicyConfiguration = Field(default_factory=RetryPolicyConfiguration)
    timeout: TimeoutConfiguration = Field(default_factory=TimeoutConfiguration)
    persona: PersonaDefaults = Field(default_factory=PersonaDefaults)
    prompt_version: PromptVersion = Field(default_factory=PromptVersion)
    quality: QualityThresholds = Field(default_factory=QualityThresholds)
    readability: ReadabilityThresholds = Field(default_factory=ReadabilityThresholds)
    validation: ValidationSettings = Field(default_factory=ValidationSettings)

    model_config = {"extra": "forbid", "frozen": True}
