from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import AuthenticationError
from app.models.auth import AuthenticatedPrincipal
from app.services.auth_service import AuthService

security = HTTPBearer(auto_error=False)


async def get_auth_service() -> AuthService:
    return AuthService()


async def get_bearer_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError("Missing bearer token")
    return credentials.credentials


async def get_authenticated_principal(
    token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthenticatedPrincipal:
    return auth_service.validate_bearer_token(token)
