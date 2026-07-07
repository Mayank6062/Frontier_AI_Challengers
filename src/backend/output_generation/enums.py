from __future__ import annotations

from enum import StrEnum


class GenerationStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    PARTIAL = "partial"


class ArtifactStatus(StrEnum):
    CREATED = "created"
    PERSISTED = "persisted"
    FAILED = "failed"
    SKIPPED = "skipped"


class BundleStatus(StrEnum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"


class PersonaType(StrEnum):
    EXECUTIVE = "executive"
    ARCHITECT = "architect"
    DEVELOPER = "developer"
    REVIEWER = "reviewer"
    AUDITOR = "auditor"
    OPERATIONS = "operations"
    JUDGE = "judge"
    PRESENTATION = "presentation"
    PRINT = "print"


class ThemeType(StrEnum):
    LIGHT = "light"
    DARK = "dark"
    PRINT = "print"


class DensityType(StrEnum):
    COMPACT = "compact"
    COMFORTABLE = "comfortable"
    SPACIOUS = "spacious"


class FailureSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FailureCategory(StrEnum):
    RENDER = "render"
    VALIDATION = "validation"
    STORAGE = "storage"
    CONFIG = "config"
    INTERNAL = "internal"


class FailureOrigin(StrEnum):
    OUTPUT = "output"
    AGENT = "agent"
    INFRA = "infra"
    UNKNOWN = "unknown"


class StageType(StrEnum):
    EXTRACT = "extract"
    RESOLVE = "resolve"
    RENDER = "render"
    VALIDATE = "validate"
    ASSEMBLE = "assemble"
    STORE = "store"


class ExecutionMode(StrEnum):
    SYNC = "sync"
    ASYNC = "async"


class ArtifactType(StrEnum):
    DOCUMENT = "document"
    DIAGRAM = "diagram"
    IMAGE = "image"
    PORTAL = "portal"
    INDEX = "index"


class SectionType(StrEnum):
    DOCUMENT = "document"
    TABLE = "table"
    DIAGRAM = "diagram"
    DASHBOARD = "dashboard"


class ArchitectureFilterCategory(StrEnum):
    ALL = "all"
    COMPONENT = "component"
    TECHNOLOGY = "technology"
    PATTERN = "pattern"


class ArchitectureSortBy(StrEnum):
    NAME = "name"
    TYPE = "type"
    CONFIDENCE = "confidence"


class VisibilityMode(StrEnum):
    VISIBLE = "visible"
    HIDDEN = "hidden"
    COLLAPSED = "collapsed"


class DependencyLayoutAlgorithm(StrEnum):
    FORCE = "force"
    HIERARCHICAL = "hierarchical"
    RADIAL = "radial"


class DependencyDirection(StrEnum):
    UPSTREAM = "upstream"
    DOWNSTREAM = "downstream"
    BOTH = "both"


class RiskSortBy(StrEnum):
    SCORE = "score"
    SEVERITY = "severity"
    CATEGORY = "category"
    STATUS = "status"


class SortDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"


class RiskCategory(StrEnum):
    SECURITY = "security"
    COST = "cost"
    COMPLIANCE = "compliance"
    DELIVERY = "delivery"
    OPERATIONAL = "operational"


class RiskStatus(StrEnum):
    OPEN = "open"
    MITIGATED = "mitigated"
    ACCEPTED = "accepted"
    DEFERRED = "deferred"


class CitationGroupBy(StrEnum):
    CATEGORY = "category"
    DOMAIN = "domain"
    AGENT = "agent"
    SECTION = "section"


class TimelineEventType(StrEnum):
    STAGE_COMPLETE = "stage_complete"
    APPROVAL = "approval"
    REFINEMENT = "refinement"
    OVERRIDE = "override"
    GOVERNANCE = "governance"


class TimelineZoomLevel(StrEnum):
    OVERVIEW = "overview"
    DETAILED = "detailed"


class TransitionType(StrEnum):
    START = "start"
    COMPLETE = "complete"
    FAIL = "fail"
    RETRY = "retry"
    PAUSE = "pause"


class RecoveryMode(StrEnum):
    RETRY = "retry"
    SKIP = "skip"
    MANUAL = "manual"
    ABORT = "abort"


class ApprovalState(StrEnum):
    DRAFT = "draft"
    APPROVED = "approved"
    REJECTED = "rejected"


class SnapshotState(StrEnum):
    VALID = "valid"
    INVALID = "invalid"
    COMPATIBLE = "compatible"
    INCOMPATIBLE = "incompatible"
