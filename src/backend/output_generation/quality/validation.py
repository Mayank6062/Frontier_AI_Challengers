from __future__ import annotations

from typing import Sequence, Optional
from pydantic import BaseModel

from .enums import ValidationSeverity


class ACQualCheck(BaseModel):
    id: str
    title: str
    description: str
    severity: ValidationSeverity = ValidationSeverity.ERROR
    owner: Optional[str] = None
    category: Optional[str] = None
    evidence_required: bool = True
    remediation: Optional[str] = None
    spec_reference: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class AC_QUAL_01(ACQualCheck):
    id: str = "AC_QUAL_01"
    title: str = "All required files present"
    description: str = (
        "Required files and sections exist in the generated bundle according to the spec."
    )
    severity: ValidationSeverity = ValidationSeverity.BLOCKER
    evidence_required: bool = True


class AC_QUAL_02(ACQualCheck):
    id: str = "AC_QUAL_02"
    title: str = "Section completeness"
    description: str = "Key sections contain expected content and headings."
    severity: ValidationSeverity = ValidationSeverity.ERROR
    evidence_required: bool = True


class AC_QUAL_03(ACQualCheck):
    id: str = "AC_QUAL_03"
    title: str = "Citation coverage"
    description: str = "All recommendations reference at least one citation ID."
    severity: ValidationSeverity = ValidationSeverity.ERROR
    evidence_required: bool = True


class AC_QUAL_04(ACQualCheck):
    id: str = "AC_QUAL_04"
    title: str = "Determinism preserved"
    description: str = "Non-AI artifacts are byte-deterministic on regeneration."
    severity: ValidationSeverity = ValidationSeverity.BLOCKER
    evidence_required: bool = True


class AC_QUAL_05(ACQualCheck):
    id: str = "AC_QUAL_05"
    title: str = "Accessibility basics"
    description: str = "Portal and artifacts meet baseline accessibility requirements."
    severity: ValidationSeverity = ValidationSeverity.ERROR
    evidence_required: bool = True


class AC_QUAL_06(ACQualCheck):
    id: str = "AC_QUAL_06"
    title: str = "Security checklist"
    description: str = "No forbidden external references and sanitization applied."
    severity: ValidationSeverity = ValidationSeverity.BLOCKER
    evidence_required: bool = True


class AC_QUAL_07(ACQualCheck):
    id: str = "AC_QUAL_07"
    title: str = "Performance budget"
    description: str = "Bundle and portal meet defined performance budgets."
    severity: ValidationSeverity = ValidationSeverity.WARN
    evidence_required: bool = True


class AC_QUAL_08(ACQualCheck):
    id: str = "AC_QUAL_08"
    title: str = "Manifest integrity"
    description: str = "Manifest contains provenance metadata and checksums."
    severity: ValidationSeverity = ValidationSeverity.ERROR
    evidence_required: bool = True


class AC_QUAL_09(ACQualCheck):
    id: str = "AC_QUAL_09"
    title: str = "Diagram validity"
    description: str = (
        "Diagrams render without external dependencies and meet shape rules."
    )
    severity: ValidationSeverity = ValidationSeverity.WARN
    evidence_required: bool = True


class AC_QUAL_10(ACQualCheck):
    id: str = "AC_QUAL_10"
    title: str = "Privacy & secrets"
    description: str = "No secrets or sensitive data are embedded in artifacts."
    severity: ValidationSeverity = ValidationSeverity.BLOCKER
    evidence_required: bool = True


class AC_QUAL_11(ACQualCheck):
    id: str = "AC_QUAL_11"
    title: str = "Template versioning"
    description: str = "Templates and versions are recorded in provenance metadata."
    severity: ValidationSeverity = ValidationSeverity.INFO
    evidence_required: bool = False


class AC_QUAL_12(ACQualCheck):
    id: str = "AC_QUAL_12"
    title: str = "Approval snapshot linkage"
    description: str = "Artifacts reference the ApprovedSnapshot id and version."
    severity: ValidationSeverity = ValidationSeverity.BLOCKER
    evidence_required: bool = True


class APQualCheck(BaseModel):
    id: str
    title: str
    description: str
    severity: ValidationSeverity = ValidationSeverity.WARN
    owner: Optional[str] = None
    evidence_required: bool = True
    remediation: Optional[str] = None
    spec_reference: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class AP_QUAL_01(APQualCheck):
    id: str = "AP_QUAL_01"
    title: str = "Anti-pattern: no LLM in renderer"
    description: str = (
        "Renderers must not call LLMs; all intelligence is upstream in agents."
    )
    severity: ValidationSeverity = ValidationSeverity.ERROR
    evidence_required: bool = True


class AP_QUAL_02(APQualCheck):
    id: str = "AP_QUAL_02"
    title: str = "Anti-pattern: external CDN references"
    description: str = "Offline portal must not reference external CDNs."
    severity: ValidationSeverity = ValidationSeverity.BLOCKER
    evidence_required: bool = True


class AP_QUAL_03(APQualCheck):
    id: str = "AP_QUAL_03"
    title: str = "Anti-pattern: mutable approved snapshot"
    description: str = (
        "ApprovedSnapshot must be immutable; generated artifacts must reference it."
    )
    severity: ValidationSeverity = ValidationSeverity.BLOCKER
    evidence_required: bool = True


class AP_QUAL_04(APQualCheck):
    id: str = "AP_QUAL_04"
    title: str = "Anti-pattern: network fetch at runtime"
    description: str = "No runtime network fetches allowed in portal artifacts."
    severity: ValidationSeverity = ValidationSeverity.BLOCKER
    evidence_required: bool = True


class AP_QUAL_05(APQualCheck):
    id: str = "AP_QUAL_05"
    title: str = "Anti-pattern: post-approval modification"
    description: str = (
        "Artifacts must not be modified after approval; any change requires new version."
    )
    severity: ValidationSeverity = ValidationSeverity.BLOCKER
    evidence_required: bool = True


class ValidationSummary(BaseModel):
    checks: Sequence[str] = ()
    passed: int = 0
    failed: int = 0

    model_config = {"extra": "forbid", "frozen": True}
