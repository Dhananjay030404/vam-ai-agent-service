from pydantic import BaseModel


class RequestContext(BaseModel):
    customer_id: str
    active_oem_id: str
    customer_oem_relation_id: str
    role: str
