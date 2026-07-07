from __future__ import annotations

import enum


class ExportFormat(enum.StrEnum):
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    DRAWIO = "drawio"
    YAML = "yaml"
    CSV = "csv"


class ExportPriority(enum.StrEnum):
    P1 = "P1"
    P2 = "P2"


class ExportStatus(enum.StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class ExportFailureReason(enum.StrEnum):
    TIMEOUT = "timeout"
    RENDER_ERROR = "render_error"
    VALIDATION_ERROR = "validation_error"
    SANITIZATION = "sanitization"


class ConverterType(enum.StrEnum):
    HTML_TO_PDF = "html_to_pdf"
    MARKDOWN_TO_DOCX = "markdown_to_docx"
    PPTX_GENERATOR = "pptx_generator"
    DRAWIO_XML = "drawio_xml"
    YAML_EXPORTER = "yaml_exporter"
    CSV_EXPORTER = "csv_exporter"


class ExportFeatureFlag(enum.StrEnum):
    EXPORT_PDF_ENABLED = "export_pdf_enabled"
    EXPORT_DOCX_ENABLED = "export_docx_enabled"
    EXPORT_PPTX_ENABLED = "export_pptx_enabled"
    EXPORT_DRAWIO_ENABLED = "export_drawio_enabled"
    EXPORT_YAML_ENABLED = "export_yaml_enabled"
    EXPORT_CSV_ENABLED = "export_csv_enabled"


class ExportCategory(enum.StrEnum):
    DOCUMENT = "document"
    DIAGRAM = "diagram"
    TOPOLOGY = "topology"


class ExportTimeoutPolicy(enum.StrEnum):
    FAIL_FAST = "fail_fast"
    RETRY_ON_TRANSIENT = "retry_on_transient"


class RetryMode(enum.StrEnum):
    NONE = "none"
    ONCE = "once"
    EXPONENTIAL = "exponential"


class ExportSeverity(enum.StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
