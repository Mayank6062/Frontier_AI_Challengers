from __future__ import annotations

from pydantic import BaseModel
from typing import Sequence

from .models import (
    DocumentMetadata,
    SectionOrderingRule,
    FormattingRule,
)


class DR01_FrontMatterContract(BaseModel):
    metadata: DocumentMetadata

    model_config = {"extra": "forbid", "frozen": True}


class DR02_CitationContract(BaseModel):
    citations: Sequence[str]

    model_config = {"extra": "forbid", "frozen": True}


class DR03_DiagramRefContract(BaseModel):
    diagram_ids: Sequence[str]

    model_config = {"extra": "forbid", "frozen": True}


class DR04_FormattingContract(BaseModel):
    rules: Sequence[FormattingRule]

    model_config = {"extra": "forbid", "frozen": True}


class DR05_OrderingContract(BaseModel):
    ordering: Sequence[SectionOrderingRule]

    model_config = {"extra": "forbid", "frozen": True}


class DR06_TemplateLocationContract(BaseModel):
    template_path: str

    model_config = {"extra": "forbid", "frozen": True}


class DR07_GoldenTestContract(BaseModel):
    golden_paths: Sequence[str]

    model_config = {"extra": "forbid", "frozen": True}


class DR08_FileNamingContract(BaseModel):
    pattern: str

    model_config = {"extra": "forbid", "frozen": True}


class DR09_NoLLMContract(BaseModel):
    enforced: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class DR10_DiagramExistsContract(BaseModel):
    required_diagram_ids: Sequence[str]

    model_config = {"extra": "forbid", "frozen": True}
