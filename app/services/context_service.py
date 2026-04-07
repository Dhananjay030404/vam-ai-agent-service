from app.core.exceptions import ContextResolutionError, AuthorizationError
from app.models.auth import AuthenticatedPrincipal
from app.models.context import RequestContext


class ContextService:
    def resolve(self, principal: AuthenticatedPrincipal) -> RequestContext:
        if not principal.active_oem_id:
            raise ContextResolutionError("Missing active OEM context")

        if not principal.customer_oem_relation_id:
            raise ContextResolutionError("Missing customer OEM relation")

        if not principal.role:
            raise AuthorizationError("Missing role")

        return RequestContext(
            customer_id=principal.customer_id,
            active_oem_id=principal.active_oem_id,
            customer_oem_relation_id=principal.customer_oem_relation_id,
            role=principal.role,
        )
