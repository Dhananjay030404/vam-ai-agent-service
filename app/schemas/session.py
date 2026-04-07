from typing import Any

from pydantic import BaseModel, Field


class SessionCreateRequest(BaseModel):
    channel: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SessionContextResponse(BaseModel):
    customer_id: str
    active_oem_id: str
    customer_oem_relation_id: str
    role: str
    allowed_tools: list[str] = Field(default_factory=list)


class SessionCreateResponse(BaseModel):
    session: SessionContextResponse
    request_id: str | None = None
