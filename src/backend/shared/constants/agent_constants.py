"""
Agent Constants — Platform-wide agent operational constants.

Provides non-secret operational defaults and limits for agent execution.
"""

# Agent execution defaults
DEFAULT_AGENT_TIMEOUT_SECONDS = 300
DEFAULT_AGENT_MAX_RETRIES = 3
DEFAULT_AGENT_RETRY_BACKOFF_MS = 100

# LLM interaction defaults (non-secret)
DEFAULT_LLM_TIMEOUT_SECONDS = 120
DEFAULT_LLM_MAX_TOKENS = 4000
DEFAULT_LLM_TEMPERATURE = 0.7

# Performance limits
MAX_CONCURRENT_AGENTS = 10
MAX_AGENT_OUTPUT_SIZE_BYTES = 1_000_000  # 1 MB

# Agent state identifiers
AGENT_STATE_PENDING = "pending"
AGENT_STATE_RUNNING = "running"
AGENT_STATE_COMPLETED = "completed"
AGENT_STATE_FAILED = "failed"
AGENT_STATE_DEGRADED = "degraded"

# Agent result status values
AGENT_STATUS_SUCCESS = "success"
AGENT_STATUS_PARTIAL = "partial"
AGENT_STATUS_FAILED = "failed"
