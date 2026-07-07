from __future__ import annotations

from typing import Dict, Optional, Sequence
from pydantic import BaseModel

from .models import ExportWarning, ExportFailure


class ValidationResult(BaseModel):
    is_valid: bool
    warnings: Sequence[ExportWarning] = ()
    failures: Sequence[ExportFailure] = ()

    model_config = {"extra": "forbid", "frozen": True}


class ValidationSummary(BaseModel):
    total_checks: int
    passed: int
    failed: int

    model_config = {"extra": "forbid", "frozen": True}


class PdfMagicValidation(BaseModel):
    magic_number_expected: str

    model_config = {"extra": "forbid", "frozen": True}


class PdfSizeValidation(BaseModel):
    max_bytes: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class DocxMacroValidation(BaseModel):
    allow_macros: bool = False

    model_config = {"extra": "forbid", "frozen": True}


class PptxAnimationValidation(BaseModel):
    allow_animations: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class DrawioXmlValidation(BaseModel):
    max_xml_length: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class YamlValidation(BaseModel):
    require_parseable: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class CsvValidation(BaseModel):
    max_rows: Optional[int]
    allow_empty: bool = False

    model_config = {"extra": "forbid", "frozen": True}


class ExportSecurityValidation(BaseModel):
    scan_for_secrets: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class ExportTimeoutValidation(BaseModel):
    max_seconds: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class ExportSanitizerValidation(BaseModel):
    rules: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}
