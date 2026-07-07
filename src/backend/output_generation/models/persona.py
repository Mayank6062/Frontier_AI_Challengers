from __future__ import annotations

from enum import Enum
from pydantic import BaseModel


class PersonaMode(str, Enum):
    AUTHOR = "author"
    REVIEWER = "reviewer"
    READER = "reader"


class Persona(BaseModel):
    id: str
    name: str
    role: PersonaMode

    model_config = {"extra": "forbid"}
