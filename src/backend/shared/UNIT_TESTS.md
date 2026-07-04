# Shared Layer Unit Tests — Test Plan

## Coverage Summary

Total Test Cases: ~100
Target Coverage: ≥85% per module
Test Execution Time: ~5-10 seconds (stdlib only)

## Test Modules

### 1. Models Tests (`models/tests/test_models.py`) — 35+ Cases

#### BaseModel (Serialization/Validation)
- ✓ `test_to_dict_basic` — Verify serialization works
- ✓ `test_from_dict_basic` — Verify deserialization works
- ✓ `test_from_dict_missing_required_field` — Error on incomplete data
- ✓ `test_equality_by_value` — Equality comparison
- ✓ `test_repr` — String representation

#### Identifier (UUID Wrapper)
- ✓ `test_generate_new_identifier` — Auto-generation
- ✓ `test_parse_valid_uuid` — Parse UUID string
- ✓ `test_parse_invalid_uuid` — Error on malformed UUID
- ✓ `test_identifier_equality` — Equality and inequality
- ✓ `test_identifier_hashable` — Use in sets/dicts
- ✓ `test_identifier_comparison` — Sorting/comparison

#### Timestamp (UTC-Only Wrapper)
- ✓ `test_generate_current_timestamp` — Current UTC
- ✓ `test_parse_utc_datetime` — Parse UTC datetime
- ✓ `test_reject_naive_datetime` — Error on naive datetime
- ✓ `test_iso_format` — ISO 8601 formatting
- ✓ `test_from_iso_format` — Parse ISO 8601
- ✓ `test_unix_timestamp` — Unix timestamp conversion
- ✓ `test_timestamp_equality` — Equality
- ✓ `test_timestamp_comparison` — Chronological ordering

#### PaginationParams (Validation)
- ✓ `test_default_pagination` — Default values
- ✓ `test_custom_pagination` — Custom values
- ✓ `test_invalid_offset` — Error on negative offset
- ✓ `test_invalid_limit` — Error on invalid limit
- ✓ `test_immutable` — Immutability enforcement

#### PaginatedResult (Generic Result Wrapper)
- ✓ `test_basic_result` — Basic result creation
- ✓ `test_empty_result` — Empty result
- ✓ `test_items_exceed_limit` — Error on size mismatch
- ✓ `test_pagination_consistency` — Consistency validation

### 2. Exceptions Tests (`exceptions/tests/test_exceptions.py`) — 15+ Cases

#### SharedError (Base Exception)
- ✓ `test_basic_error` — Error construction
- ✓ `test_error_with_code` — Custom error code
- ✓ `test_error_with_context` — Context metadata
- ✓ `test_to_dict` — Serialization
- ✓ `test_repr` — String representation
- ✓ `test_is_exception` — Inheritance

#### Derived Exceptions
- ✓ `test_validation_error` — ValidationError
- ✓ `test_serialization_error` — SerializationError
- ✓ `test_configuration_error` — ConfigurationError
- ✓ `test_dependency_error` — DependencyError
- ✓ `test_agent_error` — AgentSharedError

### 3. Utils Tests (`utils/tests/test_utils.py`) — 50+ Cases

#### TextUtils
- ✓ `test_sanitize_text_basic` — Basic sanitization
- ✓ `test_sanitize_text_removes_control_chars` — Control char removal
- ✓ `test_sanitize_text_empty_after_sanitization` — Error on empty result
- ✓ `test_sanitize_text_max_length` — Max length enforcement
- ✓ `test_truncate_text_basic` — Basic truncation
- ✓ `test_truncate_text_no_truncate_needed` — No truncation case
- ✓ `test_truncate_text_invalid_max_length` — Error on small max
- ✓ `test_escape_markdown` — Markdown escaping
- ✓ `test_pluralize_singular` — Singular form
- ✓ `test_pluralize_plural` — Plural form
- ✓ `test_pluralize_custom_plural` — Custom plural form

#### HashUtils
- ✓ `test_compute_sha256` — SHA-256 hashing
- ✓ `test_compute_sha256_deterministic` — Determinism
- ✓ `test_compute_text_hash` — Text hashing
- ✓ `test_compute_json_hash` — JSON hashing
- ✓ `test_compute_json_hash_deterministic` — JSON determinism
- ✓ `test_compute_dict_hash` — Dict hashing
- ✓ `test_stable_key` — Stable key generation

#### TimeUtils
- ✓ `test_parse_iso_timestamp` — ISO parsing
- ✓ `test_format_iso_timestamp` — ISO formatting
- ✓ `test_current_utc_timestamp` — Current UTC
- ✓ `test_parse_unix_timestamp` — Unix parsing
- ✓ `test_to_unix_timestamp` — Unix conversion
- ✓ `test_round_trip_unix` — Round-trip conversion

#### Sanitizer
- ✓ `test_sanitize_prompt_input_basic` — Basic sanitization
- ✓ `test_sanitize_prompt_removes_control_chars` — Control char removal
- ✓ `test_sanitize_prompt_removes_zero_width` — Zero-width removal
- ✓ `test_sanitize_prompt_max_length` — Max length
- ✓ `test_sanitize_json_string` — JSON sanitization
- ✓ `test_sanitize_identifier_valid` — Valid identifier
- ✓ `test_sanitize_identifier_special_chars` — Special char removal

#### RetryUtils
- ✓ `test_retry_config_basic` — Basic config
- ✓ `test_retry_config_validation` — Config validation
- ✓ `test_calculate_delay_linear` — Linear backoff
- ✓ `test_calculate_delay_exponential` — Exponential backoff
- ✓ `test_retry_decorator` — Retry decorator
- ✓ `test_retry_exhaustion` — Retry limit exhaustion

### 4. Constants Tests (`constants/tests/test_constants.py`) — 15+ Cases

#### AgentConstants
- ✓ `test_agent_states_defined` — Agent states exist
- ✓ `test_agent_statuses_defined` — Agent statuses exist
- ✓ `test_agent_timeouts_positive` — Timeouts are positive

#### EngagementConstants
- ✓ `test_engagement_states_defined` — Engagement states exist
- ✓ `test_review_outcomes_defined` — Review outcomes exist

#### PlatformConstants
- ✓ `test_headers_defined` — HTTP headers exist
- ✓ `test_pagination_defaults` — Defaults are positive
- ✓ `test_platform_info_defined` — Platform info exists

#### Limits
- ✓ `test_text_limits_positive` — Text limits positive
- ✓ `test_retry_limits_positive` — Retry limits positive
- ✓ `test_timeout_limits_positive` — Timeout limits positive

## Coverage Targets by Module

| Module | Target | Notes |
|--------|--------|-------|
| models/base_model.py | ≥90% | Serialization critical |
| models/identifier.py | ≥95% | UUID validation essential |
| models/timestamp.py | ≥95% | UTC enforcement essential |
| models/pagination.py | ≥90% | Validation critical |
| exceptions/base_exception.py | ≥90% | Error hierarchy |
| utils/text_utils.py | ≥85% | String operations |
| utils/hash_utils.py | ≥90% | Determinism critical |
| utils/retry_utils.py | ≥85% | Backoff strategies |
| utils/time_utils.py | ≥90% | Timestamp operations |
| utils/sanitizer.py | ≥85% | Security-sensitive |
| constants/ | ≥80% | Declaration-heavy |

## Running Tests

```bash
# Run all tests
pytest src/backend/shared -v --cov --cov-report=html

# Run specific module tests
pytest src/backend/shared/models -v --cov

# Run with coverage report
pytest src/backend/shared --cov=src/backend/shared --cov-report=term-missing

# Run with strict coverage gate (85% minimum)
pytest src/backend/shared --cov --cov-fail-under=85
```

## CI Integration

Pytest configuration in `pytest.ini` enforces:
- ✓ Minimum 85% coverage across all modules
- ✓ HTML coverage report generation
- ✓ Term-missing report (shows uncovered lines)
- ✓ Strict test discovery and naming conventions
- ✓ Short traceback format for clarity

## Known Limitations

- Tests use Python stdlib only (no external test dependencies per frozen spec)
- Retry decorator tests use short delays (10ms) for speed
- Timestamp tests use UTC exclusively
- No fixtures for sensitive data (secrets not tested)

## Next Steps

1. Install pytest and pytest-cov
2. Run full test suite with coverage
3. Review coverage report (htmlcov/index.html)
4. Ensure all modules meet ≥85% target
5. Gate CI pipeline on test execution and coverage
"""
Unit Tests — Shared Layer Test Suite (≥85% Coverage Target)

Authority:
    IMPLEMENTATION_SPECIFICATION.md Section 12 "CI Validation Gates"
    SHARED_LAYER_IMPLEMENTATION.md (frozen specification)

Coverage Requirements:
    - Minimum 85% line coverage per module
    - All public APIs tested
    - All error paths tested
    - All edge cases covered

Test Organization:
    src/backend/shared/models/tests/
    src/backend/shared/exceptions/tests/
    src/backend/shared/utils/tests/
    src/backend/shared/constants/tests/

Configuration:
    pytest.ini: Defines test discovery, coverage gates, reporting
    conftest.py: Per-module fixtures and configuration

Test Execution:
    pytest src/backend/shared --cov --cov-report=html
    pytest src/backend/shared/models --cov --cov-report=term-missing
"""
