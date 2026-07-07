from __future__ import annotations

from datetime import datetime
from typing import Optional, Sequence, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ..story.models import CitationReference


class _Config:
    model_config = {"extra": "forbid", "frozen": True}


class DocumentMetadata(BaseModel):
    document_id: UUID = Field(default_factory=uuid4)
    engagement_id: Optional[str]
    version: Optional[str]
    generated_at: Optional[datetime]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentHeading(BaseModel):
    level: int
    text: str

    model_config = {"extra": "forbid", "frozen": True}


class DocumentParagraph(BaseModel):
    text: str

    model_config = {"extra": "forbid", "frozen": True}


class DocumentTable(BaseModel):
    headers: Sequence[str]
    rows: Sequence[Sequence[str]]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentFigure(BaseModel):
    caption: Optional[str]
    reference: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentDiagramReference(BaseModel):
    diagram_id: str
    caption: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentCitation(CitationReference):
    model_config = {"extra": "forbid", "frozen": True}


class DocumentSection(BaseModel):
    id: str
    type: str
    heading: Optional[DocumentHeading]
    paragraphs: Sequence[DocumentParagraph] = Field(default_factory=list)
    tables: Sequence[DocumentTable] = Field(default_factory=list)
    figures: Sequence[DocumentFigure] = Field(default_factory=list)
    diagrams: Sequence[DocumentDiagramReference] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class DocumentAppendix(BaseModel):
    id: str
    content: Sequence[DocumentSection] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class DocumentIndex(BaseModel):
    citations: Sequence[DocumentCitation] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class DocumentDefinition(BaseModel):
    metadata: DocumentMetadata
    title: str
    sections: Sequence[DocumentSection]
    appendices: Optional[Sequence[DocumentAppendix]]
    index: Optional[DocumentIndex]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentFileMetadata(BaseModel):
    path: str
    size_bytes: Optional[int]
    format: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentBundle(BaseModel):
    documents: Sequence[DocumentDefinition]
    manifest_ref: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentGenerationRequest(BaseModel):
    document_type: str
    definition: DocumentDefinition
    options: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentStatistics(BaseModel):
    word_count: int
    page_count: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentGenerationSummary(BaseModel):
    document_id: UUID
    status: str
    statistics: Optional[DocumentStatistics]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentWarning(BaseModel):
    code: str
    message: str

    model_config = {"extra": "forbid", "frozen": True}


class DocumentFailure(BaseModel):
    code: str
    message: str
    category: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentGenerationResult(BaseModel):
    summary: DocumentGenerationSummary
    warnings: Sequence[DocumentWarning] = Field(default_factory=list)
    failures: Sequence[DocumentFailure] = Field(default_factory=list)
    files: Sequence[DocumentFileMetadata] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class DocumentValidationSummary(BaseModel):
    status: str
    errors: Sequence[str] = Field(default_factory=list)
    warnings: Sequence[str] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class DocumentProvenance(BaseModel):
    engagement_id: Optional[str]
    generator_version: Optional[str]
    template_version: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentVersionMetadata(BaseModel):
    version: str
    released_at: Optional[datetime]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentOutputMetadata(BaseModel):
    format: Optional[str]
    generated_at: Optional[datetime]

    model_config = {"extra": "forbid", "frozen": True}


class DocumentRenderOptions(BaseModel):
    include_toc: bool = False
    include_index: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class SectionOrderingRule(BaseModel):
    document_type: str
    section_order: Sequence[str]

    model_config = {"extra": "forbid", "frozen": True}


class FormattingRule(BaseModel):
    rule_id: str
    description: str
    mode: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class CompletenessRule(BaseModel):
    rule_id: str
    description: str
    severity: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}
