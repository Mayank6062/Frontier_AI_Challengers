"""Tests for shared exceptions."""

# pylint: disable=missing-function-docstring

from . import base_exception as _be
from .validation_exceptions import ValidationError
from .agent_exceptions import AgentError
from .knowledge_exceptions import KnowledgeError
from .ledger_exceptions import LedgerError

SharedError = _be.SharedError


def test_exception_hierarchy_and_cause() -> None:
    e = SharedError("fail", cause=ValueError("v"))
    assert isinstance(e, SharedError)
    assert isinstance(e.cause, ValueError)

    assert issubclass(ValidationError, SharedError)
    assert issubclass(AgentError, SharedError)
    assert issubclass(KnowledgeError, SharedError)
    assert issubclass(LedgerError, SharedError)
