from app.models.context import RequestContext
from app.models.session import SessionContext
from app.schemas.session import (
    SessionCreateRequest,
    SessionCreateResponse,
    SessionContextResponse,
)


class SessionService:
    def create_session(
        self,
        payload: SessionCreateRequest,
        context: RequestContext,
        allowed_tools: list[str],
        request_id: str | None,
    ) -> SessionCreateResponse:
        session = SessionContext(
            customer_id=context.customer_id,
            active_oem_id=context.active_oem_id,
            customer_oem_relation_id=context.customer_oem_relation_id,
            role=context.role,
            allowed_tools=allowed_tools,
        )
        return SessionCreateResponse(
            session=SessionContextResponse.model_validate(session.model_dump()),
            request_id=request_id,
        )
