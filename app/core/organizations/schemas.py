from pydantic import BaseModel
from enum import Enum

class SOrganizationType(str, Enum):
    IE = "IE"
    LLC = "LLC"
    JSC = "JSC"

class SOrganizationRequest(BaseModel):
    name: str
    description: str = None
    org_type: SOrganizationType