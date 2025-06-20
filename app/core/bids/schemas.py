from enum import Enum

from pydantic import BaseModel

class SBidStatus(str, Enum):
    CREATED = "CREATED"
    PUBLISHED = "PUBLISHED"


class SBidDecision(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class SBidCnceled(str, Enum):
    CANCELED = "CANCELED"


class SBidCreate(BaseModel):
    name: str
    description: str

class SBidUpdate(BaseModel):
    name: str
    description: str

class SBidFeedback(BaseModel):
    feedback: str
