"""Small retry helper for transient call retries.

This module provides a tiny retry decorator used by Shared utilities.
"""
# pylint: disable=broad-exception-caught

from __future__ import annotations

import time
from functools import wraps
from typing import Callable
from typing import TypeVar
from typing import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def retry(
    times: int = 3, delay: float = 0.0
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator to retry a synchronous function `times` with `delay` seconds between attempts.

    Note: purposely minimal. Suitable for use in Shared utilities where heavy
    frameworks are not available.
    """

    def _decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def _wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc = None
            for _ in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:  # pragma: no cover - exercised in tests
                    last_exc = exc
                    if delay:
                        time.sleep(delay)
            assert last_exc is not None
            raise last_exc

        return _wrapped

    return _decorator
