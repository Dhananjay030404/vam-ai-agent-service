from fastapi import Depends

from app.api.deps.auth import get_authenticated_principal
from app.models.auth import AuthenticatedPrincipal
from app.models.context import RequestContext
from app.services.context_service import ContextService


async def get_context_service() -> ContextService:
    return ContextService()


async def get_request_context(
    principal: AuthenticatedPrincipal = Depends(get_authenticated_principal),
    context_service: ContextService = Depends(get_context_service),
) -> RequestContext:
    return context_service.resolve(principal)
