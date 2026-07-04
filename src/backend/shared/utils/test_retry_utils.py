"""Tests for retry utilities."""

# pylint: disable=missing-function-docstring

from . import retry_utils


def test_retry_decorator_success_after_retry() -> None:
    state = {"count": 0}

    @retry_utils.retry(times=3, delay=0)
    def flaky() -> str:
        if state["count"] < 2:
            state["count"] += 1
            raise ValueError("try")
        return "ok"

    assert flaky() == "ok"
