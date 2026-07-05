from __future__ import annotations

from typing import Any, cast

import pytest

from backend.agents.base.agent_context import AgentContext


def test_agent_context_immutable() -> None:
    ctx = AgentContext(session_id="s1", execution_id="e1", metadata={"k": "v"})
    assert ctx.session_id == "s1"
    # dataclass frozen prevents attribute assignment
    with pytest.raises(Exception):
        cast(Any, ctx).session_id = "s2"
