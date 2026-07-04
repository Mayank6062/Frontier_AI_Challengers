"""
Engagement Constants — Engagement lifecycle state identifiers.

Provides canonical engagement state enumerations used throughout the platform.
"""

# Engagement states (from frozen architecture)
ENGAGEMENT_STATE_CREATED = "created"
ENGAGEMENT_STATE_DISCOVERY = "discovery"
ENGAGEMENT_STATE_DESIGN = "design"
ENGAGEMENT_STATE_VALIDATION = "validation"
ENGAGEMENT_STATE_GOVERNANCE = "governance"
ENGAGEMENT_STATE_GENERATION = "generation"
ENGAGEMENT_STATE_PENDING_HUMAN_REVIEW = "pending_human_review"
ENGAGEMENT_STATE_APPROVED = "approved"
ENGAGEMENT_STATE_REJECTED = "rejected"
ENGAGEMENT_STATE_REFINED = "refined"
ENGAGEMENT_STATE_COMPLETED = "completed"

# Human review outcomes
REVIEW_OUTCOME_APPROVED = "approved"
REVIEW_OUTCOME_REJECTED = "rejected"
REVIEW_OUTCOME_REFINE = "refine"
REVIEW_OUTCOME_OVERRIDE = "override"

# Refinement targets
REFINEMENT_TARGET_DISCOVERY = "discovery"
REFINEMENT_TARGET_DESIGN = "design"
REFINEMENT_TARGET_VALIDATION = "validation"

# Engagement result states
RESULT_STATE_DRAFT = "draft"
RESULT_STATE_APPROVED = "approved"
RESULT_STATE_ARCHIVED = "archived"
