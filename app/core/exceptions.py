class ApplicationError(Exception):
    """Base application error for predictable service failures."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthenticationError(ApplicationError):
    def __init__(self, message: str = "Invalid authentication credentials") -> None:
        super().__init__(message=message, status_code=401)


class AuthorizationError(ApplicationError):
    def __init__(self, message: str = "You are not allowed to perform this action") -> None:
        super().__init__(message=message, status_code=403)


class ContextResolutionError(ApplicationError):
    def __init__(self, message: str = "Unable to resolve session context") -> None:
        super().__init__(message=message, status_code=400)
