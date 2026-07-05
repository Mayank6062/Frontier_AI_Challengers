from backend.agents.governance.human_collaboration.proposal_packager import (
    package_proposal,
)
from backend.agents.governance.human_collaboration.feedback_router import route_feedback
from backend.agents.governance.human_collaboration.override_recorder import (
    record_override,
)


def test_human_collab_flow() -> None:
    p = package_proposal(None)
    r = route_feedback(p)
    o = record_override(None)
    assert p["title"] == "Proposal"
    assert r["status"] == "routed"
    assert o["recorded"] is True
