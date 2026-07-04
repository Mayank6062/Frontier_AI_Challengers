"""
Limits — Size and quantity limits for shared utilities.

Provides operational size and count limits used by validation and sanitization.
"""

# Text limits (bytes/characters)
MAX_TEXT_INPUT_LENGTH = 10_000
MAX_JSON_INPUT_LENGTH = 1_000_000  # 1 MB
MAX_IDENTIFIER_LENGTH = 255
MAX_CORRELATION_ID_LENGTH = 64

# Collection limits
MAX_COLLECTION_SIZE = 10_000
MAX_DICTIONARY_DEPTH = 20

# Retry limits
MAX_RETRY_ATTEMPTS = 5
MIN_RETRY_DELAY_MS = 10
MAX_RETRY_DELAY_MS = 60_000  # 60 seconds

# Timeout limits (seconds)
MIN_TIMEOUT_SECONDS = 1
MAX_TIMEOUT_SECONDS = 3600  # 1 hour

# Rate limiting
DEFAULT_RATE_LIMIT_PER_MINUTE = 100
DEFAULT_RATE_LIMIT_PER_HOUR = 5000
