from __future__ import annotations

from pydantic import BaseModel

from .contracts import (
    DR01_FrontMatterContract,
    DR02_CitationContract,
    DR03_DiagramRefContract,
    DR04_FormattingContract,
    DR05_OrderingContract,
    DR06_TemplateLocationContract,
    DR07_GoldenTestContract,
    DR08_FileNamingContract,
    DR10_DiagramExistsContract,
)


class StructureValidatorContract(BaseModel):
    ordering: DR05_OrderingContract

    model_config = {"extra": "forbid", "frozen": True}


class CitationValidatorContract(BaseModel):
    citations: DR02_CitationContract

    model_config = {"extra": "forbid", "frozen": True}


class DiagramReferenceValidatorContract(BaseModel):
    diagrams: DR03_DiagramRefContract

    model_config = {"extra": "forbid", "frozen": True}


class TemplateValidationContract(BaseModel):
    template_location: DR06_TemplateLocationContract

    model_config = {"extra": "forbid", "frozen": True}


class EncodingValidatorContract(BaseModel):
    file_naming: DR08_FileNamingContract

    model_config = {"extra": "forbid", "frozen": True}


class ProvenanceValidatorContract(BaseModel):
    front_matter: DR01_FrontMatterContract

    model_config = {"extra": "forbid", "frozen": True}


class SizeValidatorContract(BaseModel):
    golden_test: DR07_GoldenTestContract

    model_config = {"extra": "forbid", "frozen": True}


class CompletenessValidatorContract(BaseModel):
    completeness: DR10_DiagramExistsContract

    model_config = {"extra": "forbid", "frozen": True}


class FormattingValidatorContract(BaseModel):
    formatting: DR04_FormattingContract

    model_config = {"extra": "forbid", "frozen": True}


class OrderingValidatorContract(BaseModel):
    ordering: DR05_OrderingContract

    model_config = {"extra": "forbid", "frozen": True}
