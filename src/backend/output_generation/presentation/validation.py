from __future__ import annotations

from typing import Sequence
from pydantic import BaseModel


# AC-PRES (acceptance) contracts
class ACPresCheck(BaseModel):
    id: str
    description: str

    model_config = {"extra": "forbid", "frozen": True}


class AC_PRES_01(ACPresCheck):
    pass


class AC_PRES_02(ACPresCheck):
    pass


class AC_PRES_03(ACPresCheck):
    pass


class AC_PRES_04(ACPresCheck):
    pass


class AC_PRES_05(ACPresCheck):
    pass


class AC_PRES_06(ACPresCheck):
    pass


class AC_PRES_07(ACPresCheck):
    pass


class AC_PRES_08(ACPresCheck):
    pass


class AC_PRES_09(ACPresCheck):
    pass


class AC_PRES_10(ACPresCheck):
    pass


class AC_PRES_11(ACPresCheck):
    pass


class AC_PRES_12(ACPresCheck):
    pass


# AP-PRES (api/adapter) contracts
class APPresCheck(BaseModel):
    id: str
    description: str

    model_config = {"extra": "forbid", "frozen": True}


class AP_PRES_01(APPresCheck):
    pass


class AP_PRES_02(APPresCheck):
    pass


class AP_PRES_03(APPresCheck):
    pass


class AP_PRES_04(APPresCheck):
    pass


class AP_PRES_05(APPresCheck):
    pass


class AP_PRES_06(APPresCheck):
    pass


class PresentationValidationSummary(BaseModel):
    checks: Sequence[str] = ()
    passed: int = 0
    failed: int = 0

    model_config = {"extra": "forbid", "frozen": True}
