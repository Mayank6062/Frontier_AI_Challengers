from __future__ import annotations

from typing import Optional, Dict, Any
from pydantic import BaseModel


class ChatRequest(BaseModel):
    content: str
    attachments: Optional[list[str]] = None


class ChatMessage(BaseModel):
    id: str
    session_id: str
    role: str  # 'user' | 'assistant'
    content: str
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    message: ChatMessage


class ChatResponseLegacy(BaseModel):
    """Legacy response for /invoke endpoint."""
    text: str
    raw: Optional[Dict[str, Any]] = None
