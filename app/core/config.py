from dataclasses import dataclass
from functools import lru_cache
import os


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    service_name: str = "vam-ai-agent-service"
    environment: str = "local"
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    elevenlabs_api_key: str = ""
    vam_backend_base_url: str = ""
    webhook_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_issuer: str = ""
    jwt_audience: str = ""
    jwt_secret_key: str = ""
    jwt_public_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings(
        environment=os.getenv("ENVIRONMENT", "local"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        debug=_as_bool(os.getenv("DEBUG"), default=False),
        elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY", ""),
        vam_backend_base_url=os.getenv("VAM_BACKEND_BASE_URL", ""),
        webhook_secret=os.getenv("WEBHOOK_SECRET", ""),
        jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        jwt_issuer=os.getenv("JWT_ISSUER", ""),
        jwt_audience=os.getenv("JWT_AUDIENCE", ""),
        jwt_secret_key=os.getenv("JWT_SECRET_KEY", ""),
        jwt_public_key=os.getenv("JWT_PUBLIC_KEY", ""),
    )
