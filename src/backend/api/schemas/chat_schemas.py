from __future__ import annotations

from typing import Optional, Dict, Any
from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str
    model: str = "default"
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None


class ChatResponse(BaseModel):
    text: str
    raw: Optional[Dict[str, Any]] = None
