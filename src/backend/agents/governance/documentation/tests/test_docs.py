from backend.agents.governance.documentation.hld_generator import generate_hld
from backend.agents.governance.documentation.lld_generator import generate_lld
from backend.agents.governance.documentation.executive_summary_generator import (
    generate_exec,
)
from backend.agents.governance.documentation.risk_register_generator import (
    generate_risk_register,
)
from backend.agents.governance.documentation.assumptions_log_generator import (
    generate_assumptions_log,
)
from backend.agents.governance.documentation.diagram_generator import generate_diagram


def test_documentation_generators() -> None:
    assert "title" in generate_hld(None)
    assert "title" in generate_lld(None)
    assert "summary" in generate_exec(None)
    assert "risks" in generate_risk_register(None)
    assert "assumptions" in generate_assumptions_log(None)
    assert "diagram" in generate_diagram(None)
