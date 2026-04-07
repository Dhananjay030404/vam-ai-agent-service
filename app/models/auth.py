from typing import Any

from pydantic import BaseModel, Field


class AuthenticatedPrincipal(BaseModel):
    subject: str
    customer_id: str
    active_oem_id: str | None = None
    customer_oem_relation_id: str | None = None
    role: str | None = None
    claims: dict[str, Any] = Field(default_factory=dict)
