from pydantic import BaseModel
from enum import Enum

class STenderServiceType(str, Enum):
    CONSTRUCTION = "CONSTRUCTION"
    DELIVERY = "DELIVERY"
    MANUFACTURE = "MANUFACTURE"

class STenderStatus(str, Enum):
    CREATED = "CREATED"
    PUBLISHED = "PUBLISHED"
    CLOSED = "CLOSED"

class STenderCreateRequest(BaseModel):
    title: str
    description: str
    service_type: STenderServiceType

class SUpdateTenderDescription(BaseModel):
    description: str

class RollbackRequest(BaseModel):
    tender_id: str
    version: int

