from app.core.exceptions import AuthorizationError
from app.models.context import RequestContext
from app.policies.role_policy import SUPPORTED_ROLES
from app.policies.tool_policy import ROLE_TOOL_ACCESS


class PolicyService:
    def resolve_allowed_tools(self, context: RequestContext) -> list[str]:
        if not context.role:
            raise AuthorizationError("Missing role")

        if context.role not in SUPPORTED_ROLES:
            raise AuthorizationError(f"Unsupported role: {context.role}")

        return ROLE_TOOL_ACCESS[context.role]
