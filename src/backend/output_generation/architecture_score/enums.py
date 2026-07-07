from __future__ import annotations

import enum


class ScoreGrade(enum.StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


class ScoreHealthStatus(enum.StrEnum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"
    CRITICAL = "Critical"


class ScoreTrend(enum.StrEnum):
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"


class EvidenceStrength(enum.StrEnum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"


class ConfidenceLevel(enum.StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ScoreSchemaVersion(enum.StrEnum):
    V2 = "2.0.0"


class ScoreRendererMode(enum.StrEnum):
    HTML = "html"
    JSON = "json"
    MARKDOWN = "markdown"


class ScoreSeverity(enum.StrEnum):
    BLOCKER = "blocker"
    ERROR = "error"
    WARN = "warn"
    INFO = "info"
