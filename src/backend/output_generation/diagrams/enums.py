"""Diagram related enums."""

from enum import Enum


class DiagramType(str, Enum):
    SYSTEM_OVERVIEW = "system_overview"
    COMPONENT_DEPENDENCY = "component_dependency"
    DEPLOYMENT_TOPOLOGY = "deployment_topology"
    SEQUENCE = "sequence_diagram"
    STATE_MACHINE = "state_machine"
    ER = "er_diagram"
    SERVICE_MESH = "service_mesh"
    DECISION_TREE = "decision_tree"
    TIMELINE = "timeline"


class DiagramFormat(str, Enum):
    MERMAID = "mermaid"
    DOT = "dot"
    SVG = "svg"
    PNG = "png"


__all__ = ["DiagramType", "DiagramFormat"]
