"""Strongly typed settings for output-generation orchestration runtime."""

from __future__ import annotations

from dataclasses import dataclass
import os


def _read_bool(env_name: str, default: bool) -> bool:
    value = os.getenv(env_name)
    if value is None:
        return default
    normalized = value.strip().lower()
    return normalized in {"1", "true", "yes", "on"}


def _read_int(env_name: str, default: int) -> int:
    value = os.getenv(env_name)
    if value is None:
        return default
    return int(value)


def _read_float(env_name: str, default: float) -> float:
    value = os.getenv(env_name)
    if value is None:
        return default
    return float(value)


@dataclass(slots=True, frozen=True)
class RetrySettings:
    """Retry and backoff settings for orchestration stages."""

    attempts: int
    backoff_seconds: float


@dataclass(slots=True, frozen=True)
class StorageSettings:
    """Storage backend settings for output artifacts."""

    backend: str
    local_path: str
    s3_bucket: str | None


@dataclass(slots=True, frozen=True)
class TelemetrySettings:
    """Telemetry behavior and logging settings."""

    logger_name: str
    health_enabled: bool


@dataclass(slots=True, frozen=True)
class OutputGenerationSettings:
    """Root settings object for chapter 18 orchestration runtime."""

    retry: RetrySettings
    storage: StorageSettings
    telemetry: TelemetrySettings

    @classmethod
    def from_env(cls) -> "OutputGenerationSettings":
        """Build settings from environment variables."""

        retry = RetrySettings(
            attempts=_read_int("OUTPUT_GEN_RETRY_ATTEMPTS", 3),
            backoff_seconds=_read_float("OUTPUT_GEN_RETRY_BACKOFF_SECONDS", 0.5),
        )
        storage = StorageSettings(
            backend=os.getenv("OUTPUT_GEN_STORAGE_BACKEND", "local").strip().lower(),
            local_path=os.getenv("OUTPUT_GEN_LOCAL_PATH", ".output_storage").strip(),
            s3_bucket=os.getenv("OUTPUT_GEN_S3_BUCKET"),
        )
        telemetry = TelemetrySettings(
            logger_name=os.getenv("OUTPUT_GEN_LOGGER_NAME", "output_generation").strip(),
            health_enabled=_read_bool("OUTPUT_GEN_HEALTH_ENABLED", True),
        )
        settings = cls(retry=retry, storage=storage, telemetry=telemetry)
        settings.validate()
        return settings

    def validate(self) -> None:
        """Validate settings for invalid runtime combinations."""

        if self.retry.attempts < 1:
            raise ValueError("retry attempts must be >= 1")
        if self.retry.backoff_seconds < 0:
            raise ValueError("retry backoff_seconds must be >= 0")
        if self.storage.backend not in {"local", "s3"}:
            raise ValueError("storage backend must be either 'local' or 's3'")
        if self.storage.backend == "s3" and not self.storage.s3_bucket:
            raise ValueError("OUTPUT_GEN_S3_BUCKET is required when backend is 's3'")
        if not self.storage.local_path:
            raise ValueError("OUTPUT_GEN_LOCAL_PATH cannot be empty")
