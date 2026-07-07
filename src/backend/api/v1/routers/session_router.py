from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Callable
from uuid import uuid4
from datetime import datetime
import asyncio
import threading

from ...schemas.session_schemas import SessionCreateRequest, SessionResponse, SessionListResponse
from ...schemas.chat_schemas import ChatRequest, ChatResponse, ChatMessage
from ...dependencies.session_deps import get_session_manager
from ...dependencies.service_deps import DIContainer
from backend.core.session.session_manager import SessionValidationError, SessionManager
from backend.core.engagement.engagement_manager import EngagementManager
from backend.core.engagement.engagement_repository import EngagementRepository
from backend.core.interfaces.storage_interface import StorageInterface
from backend.orchestration.models import WorkflowContext
from typing import cast

router = APIRouter()


def _get_current_user_id() -> str:
    """Get the current user ID. For E2E testing, returns mock user ID."""
    # In production, this would extract from JWT token
    # For E2E testing, we use a mock user ID
    return "mock_user_123"


def _get_engagement_manager(request: Request) -> EngagementManager:
    """Get engagement manager from DI container."""
    from backend.core.engagement.engagement_repository import EngagementRepository
    provided: DIContainer.Provided = request.app.state.di_provided
    repo = EngagementRepository(cast(StorageInterface, provided.storage))
    return EngagementManager(repo)


@router.get("/", response_model=SessionListResponse)
def list_sessions(
    user_id: str = Depends(_get_current_user_id),
    mgr: "SessionManager" = Depends(get_session_manager),
) -> SessionListResponse:
    """List all sessions for the authenticated user."""
    try:
        sessions = mgr.list_sessions(user_id)
        response_sessions = []
        for s in sessions:
            session_dict = SessionResponse.from_orm(s).dict()
            session_dict["status"] = "active"
            session_dict["name"] = f"Session {s.created_at}"
            response_sessions.append(session_dict)
        
        return SessionListResponse(
            sessions=response_sessions,
            total=len(sessions),
            limit=100,
            offset=0,
        )
    except SessionValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    req: SessionCreateRequest, mgr: "SessionManager" = Depends(get_session_manager)
) -> SessionResponse:
    try:
        s = mgr.create_session(req.user_id, ttl_seconds=req.ttl_seconds, data=req.data)
        return SessionResponse.from_orm(s)
    except SessionValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(
    session_id: str, mgr: "SessionManager" = Depends(get_session_manager)
) -> SessionResponse:
    try:
        s = mgr.get_session(session_id)
        return SessionResponse.from_orm(s)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/{session_id}/chat/message", response_model=ChatResponse)
def submit_chat_message(
    session_id: str,
    req: ChatRequest,
    session_mgr: "SessionManager" = Depends(get_session_manager),
    request: Request = None,
) -> ChatResponse:
    """Submit a chat message for a session. Creates an engagement and triggers the workflow engine."""
    try:
        print(f"[MESSAGE_ENDPOINT] Received message for session {session_id}: {req.content}")
        
        # Validate session exists
        session = session_mgr.get_session(session_id)
        print(f"[MESSAGE_ENDPOINT] Session found: {session.id}")
        
        # Create the user message to return immediately
        user_message = ChatMessage(
            id=str(uuid4()),
            session_id=session_id,
            role="user",
            content=req.content,
            timestamp=datetime.utcnow().isoformat(),
        )
        
        # NOW: Trigger the workflow engine asynchronously
        if request and request.app.state.di_provided:
            try:
                print(f"[MESSAGE_ENDPOINT] Triggering workflow engine for message")
                provided: DIContainer.Provided = request.app.state.di_provided
                
                # Create an engagement for this message
                engagement_repo = EngagementRepository(
                    cast(StorageInterface, provided.storage)
                )
                engagement_mgr = EngagementManager(engagement_repo)
                engagement = engagement_mgr.create(
                    title=f"Chat: {req.content[:50]}",
                    description=f"User message in session {session_id}"
                )
                print(f"[MESSAGE_ENDPOINT] Created engagement: {engagement.id}")
                
                # Build the workflow context
                ctx = WorkflowContext(
                    engagement_id=engagement.id,
                    input_payload={
                        "user_message": req.content,
                        "session_id": session_id,
                        "message_id": user_message.id,
                    }
                )
                
                # Run the workflow asynchronously
                def run_workflow():
                    try:
                        print(f"[WORKFLOW] Starting for engagement {engagement.id}")
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            def checkpoint_writer(eid, group, results):
                                print(f"[WORKFLOW] Checkpoint: {eid} - Group {group} completed")
                                for r in results:
                                    print(f"  Stage {r.stage_id}: {r.status} - {r.output}")
                            
                            results = loop.run_until_complete(
                                provided.master_orchestrator.run_phase(ctx, checkpoint_writer)
                            )
                            print(f"[WORKFLOW] Completed for engagement {engagement.id}")
                            print(f"[WORKFLOW] Results: {len(results)} stages")
                            for r in results:
                                print(f"  Stage {r.stage_id}: {r.status}")
                                if r.output:
                                    print(f"    Output: {list(r.output.keys())}")
                        finally:
                            loop.close()
                    except Exception as e:
                        print(f"[WORKFLOW] Error for engagement {engagement.id}: {e}")
                        import traceback
                        traceback.print_exc()
                
                # Start workflow in a background thread
                workflow_thread = threading.Thread(target=run_workflow, daemon=True)
                workflow_thread.start()
                print(f"[MESSAGE_ENDPOINT] Workflow started in background thread")
            except Exception as e:
                print(f"[MESSAGE_ENDPOINT] Failed to trigger workflow: {e}")
                import traceback
                traceback.print_exc()
                # Don't fail the message endpoint - still return the user message
        
        response = ChatResponse(message=user_message)
        print(f"[MESSAGE_ENDPOINT] Returning response: {response.message.id}")
        return response
    except SessionValidationError as exc:
        print(f"[MESSAGE_ENDPOINT] Session validation error: {exc}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        print(f"[MESSAGE_ENDPOINT] Unexpected error: {exc}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
