"""
Retry Utils — Retry and backoff primitives.

Provides retry/backoff factories and decorators for operation retry logic.
Responsibility: Offer deterministic retry strategies without external IO.
"""

import random
import time
from enum import Enum
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")


class BackoffStrategy(Enum):
    """Backoff strategy enumeration."""

    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    RANDOM = "random"


class RetryConfig:
    """
    Configuration for retry operations.

    Attributes:
        max_attempts: Maximum number of attempts.
        initial_delay_ms: Initial delay in milliseconds.
        max_delay_ms: Maximum delay in milliseconds.
        backoff_strategy: Backoff strategy to use.
        jitter: Whether to add random jitter to delays.
    """

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay_ms: int = 100,
        max_delay_ms: int = 5000,
        backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL,
        jitter: bool = True,
    ):
        """Initialize retry configuration."""
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        if initial_delay_ms < 1:
            raise ValueError("initial_delay_ms must be >= 1")
        if max_delay_ms < initial_delay_ms:
            raise ValueError("max_delay_ms must be >= initial_delay_ms")

        self.max_attempts = max_attempts
        self.initial_delay_ms = initial_delay_ms
        self.max_delay_ms = max_delay_ms
        self.backoff_strategy = backoff_strategy
        self.jitter = jitter

    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for attempt (in seconds).

        Args:
            attempt: Zero-based attempt number.

        Returns:
            Delay in seconds.
        """
        if attempt < 0:
            raise ValueError("attempt must be non-negative")

        if self.backoff_strategy == BackoffStrategy.LINEAR:
            delay_ms = self.initial_delay_ms * (attempt + 1)
        elif self.backoff_strategy == BackoffStrategy.EXPONENTIAL:
            delay_ms = self.initial_delay_ms * (2 ** attempt)
        elif self.backoff_strategy == BackoffStrategy.RANDOM:
            delay_ms = random.randint(self.initial_delay_ms, self.max_delay_ms)
        else:
            raise ValueError(f"Unknown backoff strategy: {self.backoff_strategy}")

        delay_ms = min(delay_ms, self.max_delay_ms)

        if self.jitter:
            jitter_ms = random.randint(0, int(delay_ms * 0.1))
            delay_ms += jitter_ms

        return delay_ms / 1000.0


def retry_with_backoff(
    config: Optional[RetryConfig] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for retrying function with backoff.

    Args:
        config: RetryConfig instance (default: standard config).

    Returns:
        Decorator function.

    Example:
        @retry_with_backoff()
        def flaky_operation():
            ...
    """
    if config is None:
        config = RetryConfig()

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Optional[Exception] = None

            for attempt in range(config.max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < config.max_attempts - 1:
                        delay = config.calculate_delay(attempt)
                        time.sleep(delay)

            raise last_exception or RuntimeError("Retry exhausted with no exception")

        return wrapper

    return decorator
