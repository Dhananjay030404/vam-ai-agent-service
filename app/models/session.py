from pydantic import BaseModel, Field


class SessionContext(BaseModel):
    customer_id: str
    active_oem_id: str
    customer_oem_relation_id: str
    role: str
    allowed_tools: list[str] = Field(default_factory=list)
