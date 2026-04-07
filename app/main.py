from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.session import router as session_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.middleware.error_handler import register_exception_handlers
from app.middleware.request_id import RequestIDMiddleware


def create_application() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    application = FastAPI(
        title="VAM AI Agent Service",
        version="0.1.0",
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url="/redoc" if settings.environment != "production" else None,
    )

    application.state.settings = settings
    application.add_middleware(RequestIDMiddleware)
    application.include_router(health_router)
    application.include_router(session_router)
    register_exception_handlers(application)

    logger = get_logger(__name__)

    @application.on_event("startup")
    async def on_startup() -> None:
        logger.info(
            "application_startup",
            extra={
                "environment": settings.environment,
                "service_name": settings.service_name,
            },
        )

    return application


app = create_application()
