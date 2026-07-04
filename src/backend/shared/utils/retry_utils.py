"""
Small retry helper for transient call retries.
"""
from __future__ import annotations

import time
from functools import wraps
from typing import Callable


def retry(times: int = 3, delay: float = 0.0):
    """Decorator to retry a synchronous function `times` with `delay` seconds between attempts.

    Note: purposely minimal; suitable for use in shared utilities where heavy frameworks are not allowed.
    """
    def _decorator(fn: Callable):
        @wraps(fn)
        def _wrapped(*args, **kwargs):
            last_exc = None
            for _ in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:  # pragma: no cover - exercised in tests
                    last_exc = exc
                    if delay:
                        time.sleep(delay)
            if last_exc is not None:
                raise last_exc

        return _wrapped

    return _decorator

