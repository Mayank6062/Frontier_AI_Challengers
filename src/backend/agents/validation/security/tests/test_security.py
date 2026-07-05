from backend.agents.validation.security.threat_modeler import generate_threat_model
from backend.agents.validation.security.control_mapper import map_controls
from backend.agents.validation.security.finding_classifier import classify_findings


def test_threat_model_basic() -> None:
    t = generate_threat_model(None)
    assert any(th["id"] == "T01" for th in t)


def test_control_mapper_and_finding_classifier() -> None:
    threats = generate_threat_model(None)
    controls = map_controls(threats)
    findings = classify_findings(threats)
    assert isinstance(controls, list)
    assert isinstance(findings, list)
