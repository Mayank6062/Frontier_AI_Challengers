from __future__ import annotations

import enum


class DocumentType(enum.StrEnum):
    DOC_01_HLD = "DOC-01-HLD"
    DOC_02_LLD = "DOC-02-LLD"
    DOC_03_EXEC = "DOC-03-EXEC"
    DOC_04_ARCH = "DOC-04-ARCH"
    DOC_05_IMPL = "DOC-05-IMPL"
    DOC_06_RISK = "DOC-06-RISK"
    DOC_07_COMPLIANCE = "DOC-07-COMP"
    DOC_08_COST = "DOC-08-COST"
    DOC_09_DECISION = "DOC-09-DEC"
    DOC_10_TECH = "DOC-10-TECH"
    DOC_11_STORY = "DOC-11-STORY"


class DocumentStatus(enum.StrEnum):
    DRAFT = "draft"
    VALIDATED = "validated"
    PUBLISHED = "published"


class DocumentFormat(enum.StrEnum):
    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"


class DocumentPersona(enum.StrEnum):
    ARCHITECT = "architect"
    DEVELOPER = "developer"
    EXECUTIVE = "executive"
    AUDITOR = "auditor"


class DocumentSectionType(enum.StrEnum):
    METADATA = "metadata"
    EXEC_SUMMARY = "executive_summary"
    PROBLEM = "problem_statement"
    ARCH_OVERVIEW = "architecture_overview"
    COMPONENT = "component"
    RISK = "risk"
    APPENDIX = "appendix"


class DocumentValidationStatus(enum.StrEnum):
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"


class DocumentGeneratorType(enum.StrEnum):
    MARKDOWN = "markdown_generator"
    HTML = "html_generator"


class DocumentSeverity(enum.StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class DocumentFailureCategory(enum.StrEnum):
    MISSING = "missing"
    INVALID = "invalid"
    TIMING = "timing"


class TemplateResolutionReason(enum.StrEnum):
    MISSING_SOURCE = "missing_source"
    GENERATION_FAILED = "generation_failed"


class HeadingLevel(enum.IntEnum):
    H1 = 1
    H2 = 2
    H3 = 3
    H4 = 4


class FormattingMode(enum.StrEnum):
    GFM = "gfm"
    PLAIN = "plain"


class TemplateVersion(enum.StrEnum):
    V1 = "v1"
    V2 = "v2"


class DocumentPriority(enum.StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
