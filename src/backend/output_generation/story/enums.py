from __future__ import annotations

from enum import StrEnum


class NarrativeDepth(StrEnum):
    SUMMARY = "summary"
    DETAILED = "detailed"
    FULL = "full"


class NarrativeTone(StrEnum):
    NEUTRAL = "neutral"
    TECHNICAL = "technical"
    PERSUASIVE = "persuasive"
    CONCISE = "concise"


class NarrativeSectionType(StrEnum):
    INTRODUCTION = "introduction"
    BACKGROUND = "background"
    DECISION = "decision"
    ALTERNATIVE = "alternative"
    COMPONENT = "component"
    WALKTHROUGH = "walkthrough"


class NarrativeStatus(StrEnum):
    DRAFT = "draft"
    REVIEW = "review"
    FINAL = "final"


class NarrativeValidationStatus(StrEnum):
    UNKNOWN = "unknown"
    PASSED = "passed"
    FAILED = "failed"


class NarrativeFailureSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NarrativeFailureCategory(StrEnum):
    CONTENT = "content"
    CITATION = "citation"
    STRUCTURE = "structure"
    QUALITY = "quality"


class NarrativeGenerationMode(StrEnum):
    AUTO = "auto"
    ASSISTED = "assisted"
    MANUAL = "manual"


class NarrativePersonaType(StrEnum):
    AUTHOR = "author"
    REVIEWER = "reviewer"
    AUDIENCE = "audience"


class NarrativeConfidenceLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
