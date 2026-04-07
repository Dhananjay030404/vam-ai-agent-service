from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.core.exceptions import AuthenticationError
from app.models.auth import AuthenticatedPrincipal


class TokenValidator(Protocol):
    def validate(self, token: str) -> AuthenticatedPrincipal: ...


@dataclass
class LocalTokenValidator:
    """
    Local-only token format:
    local:<customer_id>:<active_oem_id>:<customer_oem_relation_id>:<role>
    """

    prefix: str = "local:"

    def validate(self, token: str) -> AuthenticatedPrincipal:
        if not token or not token.startswith(self.prefix):
            raise AuthenticationError("Invalid token")

        parts = token.split(":")
        if len(parts) != 5:
            raise AuthenticationError("Invalid token")

        _, customer_id, active_oem_id, relation_id, role = parts
        if not customer_id:
            raise AuthenticationError("Invalid token")

        return AuthenticatedPrincipal(
            subject=customer_id,
            customer_id=customer_id,
            active_oem_id=active_oem_id or None,
            customer_oem_relation_id=relation_id or None,
            role=role or None,
            claims={"provider": "local-stub"},
        )


class AuthService:
    def __init__(self, validator: TokenValidator | None = None) -> None:
        self.validator = validator or LocalTokenValidator()

    def validate_bearer_token(self, token: str) -> AuthenticatedPrincipal:
        return self.validator.validate(token)
