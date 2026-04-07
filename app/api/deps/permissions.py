from fastapi import Depends

from app.api.deps.context import get_request_context
from app.models.context import RequestContext
from app.services.policy_service import PolicyService
from app.services.session_service import SessionService


async def get_policy_service() -> PolicyService:
    return PolicyService()


async def get_session_service() -> SessionService:
    return SessionService()


async def get_allowed_tools(
    context: RequestContext = Depends(get_request_context),
    policy_service: PolicyService = Depends(get_policy_service),
) -> list[str]:
    return policy_service.resolve_allowed_tools(context)
