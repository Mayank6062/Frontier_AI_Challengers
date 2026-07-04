from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from ...schemas.output_schemas import OutputRequest, OutputResponse
from ...dependencies.service_deps import DIContainer

router = APIRouter()


def _logger_provider(request: Request):
    provided: DIContainer.Provided = request.app.state.di_provided
    return provided.logger


@router.post("/render", response_model=OutputResponse)
def render_output(req: OutputRequest, logger=Depends(_logger_provider)) -> OutputResponse:
    # The API layer logs the request and returns a simple acknowledgement.
    logger.emit_log("info", "render_output", {"size": len(req.payload)})
    return OutputResponse(status="accepted")
