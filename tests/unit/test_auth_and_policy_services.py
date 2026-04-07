from app.core.exceptions import AuthenticationError, AuthorizationError, ContextResolutionError
from app.models.auth import AuthenticatedPrincipal
from app.models.context import RequestContext
from app.services.auth_service import AuthService
from app.services.context_service import ContextService
from app.services.policy_service import PolicyService


def test_auth_service_validates_local_token() -> None:
    service = AuthService()

    principal = service.validate_bearer_token(
        "local:customer-123:oem-456:relation-789:service_advisor"
    )

    assert principal.customer_id == "customer-123"
    assert principal.active_oem_id == "oem-456"
    assert principal.customer_oem_relation_id == "relation-789"
    assert principal.role == "service_advisor"


def test_auth_service_rejects_invalid_token() -> None:
    service = AuthService()

    try:
        service.validate_bearer_token("invalid-token")
    except AuthenticationError as exc:
        assert exc.status_code == 401
        assert exc.message == "Invalid token"
    else:
        raise AssertionError("Expected invalid token to raise AuthenticationError")


def test_context_service_requires_active_oem() -> None:
    service = ContextService()
    principal = AuthenticatedPrincipal(
        subject="customer-123",
        customer_id="customer-123",
        active_oem_id=None,
        customer_oem_relation_id="relation-789",
        role="service_advisor",
    )

    try:
        service.resolve(principal)
    except ContextResolutionError as exc:
        assert exc.message == "Missing active OEM context"
    else:
        raise AssertionError("Expected missing OEM context to fail")


def test_policy_service_rejects_unsupported_role() -> None:
    service = PolicyService()
    context = RequestContext(
        customer_id="customer-123",
        active_oem_id="oem-456",
        customer_oem_relation_id="relation-789",
        role="unknown_role",
    )

    try:
        service.resolve_allowed_tools(context)
    except AuthorizationError as exc:
        assert exc.message == "Unsupported role: unknown_role"
    else:
        raise AssertionError("Expected unsupported role to fail")
