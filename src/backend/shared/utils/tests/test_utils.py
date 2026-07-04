"""Unit tests for utils module."""

import pytest
import time
from datetime import datetime, timezone, timedelta

from ..text_utils import sanitize_text, truncate_text, escape_markdown, pluralize
from ..hash_utils import compute_sha256, compute_text_hash, compute_json_hash, compute_dict_hash, stable_key
from ..time_utils import (
    parse_iso_timestamp,
    format_iso_timestamp,
    current_utc_timestamp,
    parse_unix_timestamp,
    to_unix_timestamp,
)
from ..sanitizer import sanitize_prompt_input, sanitize_json_string, sanitize_identifier
from ..retry_utils import RetryConfig, BackoffStrategy, retry_with_backoff


class TestTextUtils:
    """Tests for text utilities."""

    def test_sanitize_text_basic(self):
        """Test basic text sanitization."""
        result = sanitize_text("  hello   world  ")
        assert result == "hello world"

    def test_sanitize_text_removes_control_chars(self):
        """Test removal of control characters."""
        text = "hello\x00\x01world"
        result = sanitize_text(text)
        assert "\x00" not in result
        assert "\x01" not in result

    def test_sanitize_text_empty_after_sanitization(self):
        """Test error on empty after sanitization."""
        with pytest.raises(ValueError, match="becomes empty"):
            sanitize_text("   \t\n  ")

    def test_sanitize_text_max_length(self):
        """Test truncation to max length."""
        result = sanitize_text("hello world", max_length=5)
        assert len(result) <= 5

    def test_truncate_text_basic(self):
        """Test basic text truncation."""
        result = truncate_text("hello world", max_length=8)
        assert result == "hello..."

    def test_truncate_text_no_truncate_needed(self):
        """Test no truncation when not needed."""
        result = truncate_text("hello", max_length=10)
        assert result == "hello"

    def test_truncate_text_invalid_max_length(self):
        """Test error on max_length too small."""
        with pytest.raises(ValueError, match="max_length"):
            truncate_text("hello", max_length=2)

    def test_escape_markdown(self):
        """Test Markdown escaping."""
        result = escape_markdown("**bold** *italic* `code`")
        assert "\\*" in result
        assert "\\`" in result

    def test_pluralize_singular(self):
        """Test pluralize with singular count."""
        result = pluralize(1, "item")
        assert result == "item"

    def test_pluralize_plural(self):
        """Test pluralize with plural count."""
        result = pluralize(2, "item")
        assert result == "items"

    def test_pluralize_custom_plural(self):
        """Test pluralize with custom plural form."""
        result = pluralize(2, "child", plural="children")
        assert result == "children"


class TestHashUtils:
    """Tests for hash utilities."""

    def test_compute_sha256(self):
        """Test SHA-256 hashing."""
        data = b"test data"
        result = compute_sha256(data)
        assert len(result) == 64  # SHA-256 hex is 64 chars
        assert isinstance(result, str)

    def test_compute_sha256_deterministic(self):
        """Test deterministic hashing."""
        result1 = compute_sha256(b"test")
        result2 = compute_sha256(b"test")
        assert result1 == result2

    def test_compute_text_hash(self):
        """Test text hashing."""
        result = compute_text_hash("test data")
        assert len(result) == 64
        assert isinstance(result, str)

    def test_compute_json_hash(self):
        """Test JSON hashing."""
        obj = {"key": "value", "count": 42}
        result = compute_json_hash(obj)
        assert len(result) == 64

    def test_compute_json_hash_deterministic(self):
        """Test deterministic JSON hashing."""
        obj1 = {"b": 2, "a": 1}
        obj2 = {"a": 1, "b": 2}
        result1 = compute_json_hash(obj1)
        result2 = compute_json_hash(obj2)
        assert result1 == result2  # Same despite different order

    def test_compute_dict_hash(self):
        """Test dict hashing."""
        data = {"key": "value"}
        result = compute_dict_hash(data)
        assert len(result) == 64

    def test_stable_key(self):
        """Test stable key generation."""
        key1 = stable_key("part1", "part2", 42)
        key2 = stable_key("part1", "part2", 42)
        assert key1 == key2
        assert len(key1) == 64


class TestTimeUtils:
    """Tests for time utilities."""

    def test_parse_iso_timestamp(self):
        """Test ISO timestamp parsing."""
        iso_str = "2026-07-04T12:00:00+00:00"
        dt = parse_iso_timestamp(iso_str)
        assert dt.year == 2026
        assert dt.month == 7
        assert dt.day == 4

    def test_format_iso_timestamp(self):
        """Test ISO timestamp formatting."""
        dt = datetime(2026, 7, 4, 12, 0, 0, tzinfo=timezone.utc)
        result = format_iso_timestamp(dt)
        assert "2026-07-04" in result
        assert "12:00:00" in result

    def test_current_utc_timestamp(self):
        """Test current UTC timestamp."""
        ts = current_utc_timestamp()
        assert ts.tzinfo == timezone.utc

    def test_parse_unix_timestamp(self):
        """Test Unix timestamp parsing."""
        unix_ts = 1751712000.0  # 2026-07-04 12:00:00 UTC
        dt = parse_unix_timestamp(unix_ts)
        assert dt.tzinfo == timezone.utc

    def test_to_unix_timestamp(self):
        """Test conversion to Unix timestamp."""
        dt = datetime(2026, 7, 4, 12, 0, 0, tzinfo=timezone.utc)
        result = to_unix_timestamp(dt)
        assert isinstance(result, float)
        assert result > 0

    def test_round_trip_unix(self):
        """Test round-trip Unix timestamp conversion."""
        dt = datetime(2026, 7, 4, 12, 0, 0, tzinfo=timezone.utc)
        unix_ts = to_unix_timestamp(dt)
        dt_restored = parse_unix_timestamp(unix_ts)
        assert dt_restored == dt


class TestSanitizer:
    """Tests for input sanitizer."""

    def test_sanitize_prompt_input_basic(self):
        """Test basic prompt input sanitization."""
        result = sanitize_prompt_input("hello world")
        assert result == "hello world"

    def test_sanitize_prompt_removes_control_chars(self):
        """Test removal of control characters from prompt."""
        text = "hello\x00world\x1ftest"
        result = sanitize_prompt_input(text)
        assert "\x00" not in result
        assert "\x1f" not in result

    def test_sanitize_prompt_removes_zero_width(self):
        """Test removal of zero-width characters."""
        text = "hello\u200bworld"  # Zero-width space
        result = sanitize_prompt_input(text)
        assert "\u200b" not in result

    def test_sanitize_prompt_max_length(self):
        """Test max length enforcement."""
        result = sanitize_prompt_input("x" * 20000, max_length=100)
        assert len(result) <= 100

    def test_sanitize_json_string(self):
        """Test JSON string sanitization."""
        result = sanitize_json_string("hello world")
        assert result == "hello world"

    def test_sanitize_identifier_valid(self):
        """Test identifier sanitization."""
        result = sanitize_identifier("my_var_123")
        assert result == "my_var_123"

    def test_sanitize_identifier_special_chars(self):
        """Test identifier sanitization removes special chars."""
        result = sanitize_identifier("my-var@123!")
        assert "@" not in result
        assert "!" not in result


class TestRetryUtils:
    """Tests for retry utilities."""

    def test_retry_config_basic(self):
        """Test basic RetryConfig."""
        config = RetryConfig()
        assert config.max_attempts == 3
        assert config.initial_delay_ms == 100

    def test_retry_config_validation(self):
        """Test RetryConfig validation."""
        with pytest.raises(ValueError):
            RetryConfig(max_attempts=0)

    def test_calculate_delay_linear(self):
        """Test linear backoff calculation."""
        config = RetryConfig(backoff_strategy=BackoffStrategy.LINEAR, jitter=False)
        delay1 = config.calculate_delay(0)
        delay2 = config.calculate_delay(1)
        assert delay2 > delay1

    def test_calculate_delay_exponential(self):
        """Test exponential backoff calculation."""
        config = RetryConfig(backoff_strategy=BackoffStrategy.EXPONENTIAL, jitter=False)
        delay1 = config.calculate_delay(0)
        delay2 = config.calculate_delay(1)
        delay3 = config.calculate_delay(2)
        assert delay2 > delay1
        assert delay3 > delay2

    def test_retry_decorator(self):
        """Test retry decorator."""
        call_count = 0

        @retry_with_backoff(RetryConfig(max_attempts=3, initial_delay_ms=10, jitter=False))
        def flaky_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Not yet")
            return "success"

        result = flaky_function()
        assert result == "success"
        assert call_count == 3

    def test_retry_exhaustion(self):
        """Test retry exhaustion."""
        @retry_with_backoff(RetryConfig(max_attempts=2, initial_delay_ms=10, jitter=False))
        def always_fails():
            raise ValueError("Always fails")

        with pytest.raises(ValueError, match="Always fails"):
            always_fails()
