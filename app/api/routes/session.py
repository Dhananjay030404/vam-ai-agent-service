from fastapi import APIRouter, Depends, Request

from app.api.deps.context import get_request_context
from app.api.deps.permissions import get_allowed_tools, get_session_service
from app.models.context import RequestContext
from app.schemas.session import SessionCreateRequest, SessionCreateResponse
from app.services.session_service import SessionService

router = APIRouter(prefix="/api/v1", tags=["session"])


@router.post("/session", response_model=SessionCreateResponse)
async def create_session(
    payload: SessionCreateRequest,
    request: Request,
    context: RequestContext = Depends(get_request_context),
    allowed_tools: list[str] = Depends(get_allowed_tools),
    session_service: SessionService = Depends(get_session_service),
) -> SessionCreateResponse:
    request_id = getattr(request.state, "request_id", None)
    return session_service.create_session(
        payload=payload,
        context=context,
        allowed_tools=allowed_tools,
        request_id=request_id,
    )
