from __future__ import annotations

from typing import Optional, Sequence
from pydantic import BaseModel, Field

# NV-01 .. NV-08 validation contract data models (data-only)


class NV01_MetadataContract(BaseModel):
    id: str
    required_fields: Sequence[str] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class NV02_CitationContract(BaseModel):
    allow_external: bool = False
    required_formats: Sequence[str] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class NV03_StructureContract(BaseModel):
    max_sections: int = 20
    required_section_types: Sequence[str] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class NV04_QualityContract(BaseModel):
    min_readability: Optional[float] = None
    min_confidence: Optional[float] = None

    model_config = {"extra": "forbid", "frozen": True}


class NV05_PersonaContract(BaseModel):
    allowed_personas: Sequence[str] = Field(default_factory=list)
    default_persona: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class NV06_RetryContract(BaseModel):
    max_retries: int = 0
    backoff_seconds: Optional[int] = None

    model_config = {"extra": "forbid", "frozen": True}


class NV07_TimingContract(BaseModel):
    timeout_seconds: Optional[int] = None

    model_config = {"extra": "forbid", "frozen": True}


class NV08_ProvenanceContract(BaseModel):
    require_provenance: bool = True
    allowed_sources: Sequence[str] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}
