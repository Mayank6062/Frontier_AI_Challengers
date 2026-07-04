from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status, Request

from ...schemas.chat_schemas import ChatRequest, ChatResponse
from ...dependencies.service_deps import DIContainer
from backend.core.interfaces.llm_interface import LLMInterface

router = APIRouter()


def _llm_provider(request: Request) -> LLMInterface:
    provided: DIContainer.Provided = request.app.state.di_provided
    return provided.llm


@router.post("/invoke", response_model=ChatResponse)
def invoke_chat(req: ChatRequest, llm=Depends(_llm_provider)) -> ChatResponse:
    # Delegates to LLMInterface; keeps no orchestration
    resp = llm.invoke(req.prompt, req.model)
    return ChatResponse(text=resp.text, raw=resp.raw)
