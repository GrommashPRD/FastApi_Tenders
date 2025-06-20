from sqlalchemy import Column, String, ForeignKey, Enum, DateTime
from app.database import Base
from sqlalchemy.sql import func
import enum
import uuid

class OrganizationType(enum.Enum):
    IE = "IE"
    LLC = "LLC"
    JSC = "JSC"

class Organization(Base):
    __tablename__ = "organization"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(String)
    type = Column(Enum(OrganizationType))
    organization_owner = Column(String, ForeignKey("employee.username"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())

class OrganizationResponsible(Base):
    __tablename__ = "organization_responsible"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String, ForeignKey("organization.id"), nullable=False)
    user_id = Column(String, ForeignKey("employee.id"), nullable=False)