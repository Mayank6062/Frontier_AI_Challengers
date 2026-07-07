from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel


class PdfSettings(BaseModel):
    enable_hyperlinks: bool = True
    max_pages: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class DocxSettings(BaseModel):
    allow_macros: bool = False
    max_size_bytes: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class PptxSettings(BaseModel):
    max_slides: Optional[int]
    allow_animations: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class DrawioSettings(BaseModel):
    max_xml_length: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class YamlSettings(BaseModel):
    preserve_order: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class CsvSettings(BaseModel):
    delimiter: str = ","
    max_rows: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class SecuritySettings(BaseModel):
    scan_for_secrets: bool = True
    allow_external_references: bool = False

    model_config = {"extra": "forbid", "frozen": True}


class PerformanceSettings(BaseModel):
    max_workers: Optional[int]
    memory_limit_mb: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class ExportSettings(BaseModel):
    pdf: Optional[PdfSettings]
    docx: Optional[DocxSettings]
    pptx: Optional[PptxSettings]
    drawio: Optional[DrawioSettings]
    yaml: Optional[YamlSettings]
    csv: Optional[CsvSettings]
    security: Optional[SecuritySettings]
    performance: Optional[PerformanceSettings]
    extra: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}
