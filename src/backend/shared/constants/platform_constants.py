"""
Platform Constants — Global platform-wide constants.

Provides shared constants for headers, formats, and operational defaults.
"""

# HTTP Headers
CORRELATION_ID_HEADER = "X-Correlation-ID"
REQUEST_ID_HEADER = "X-Request-ID"
TRACE_ID_HEADER = "X-Trace-ID"

# Timestamp formats
ISO_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

# Default pagination
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 1000
MIN_PAGE_SIZE = 1

# Content types
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_MARKDOWN = "text/markdown"
CONTENT_TYPE_HTML = "text/html"
CONTENT_TYPE_PDF = "application/pdf"

# Platform identifiers and versions
PLATFORM_NAME = "ArchitectIQ"
PLATFORM_VERSION = "1.0.0"
API_VERSION = "v1"

# Logging levels (as strings for consistency)
LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_ERROR = "ERROR"
LOG_LEVEL_CRITICAL = "CRITICAL"
