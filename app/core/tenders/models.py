from sqlalchemy import Column, String, Integer,Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database import Base
import enum
import uuid


class TenderStatus(enum.Enum):
    CREATED = "CREATED"
    PUBLISHED = "PUBLISHED"
    CLOSED = "CLOSED"

class TenderServiceType(enum.Enum):
    CONSTRUCTION = "CONSTRUCTION"
    DELIVERY = "DELIVERY"
    MANUFACTURE = "MANUFACTURE"



class TenderVersion(Base):
    __tablename__ = 'tender_versions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id = Column(UUID(as_uuid=True), ForeignKey('tenders.id'), nullable=False)
    version = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tender = relationship("Tender", back_populates="versions")


class Tender(Base):
    __tablename__ = 'tenders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    service_type = Column(Enum(TenderServiceType))
    version = Column(Integer, default=1, nullable=False)
    status = Column(Enum(TenderStatus), default=TenderStatus.CREATED)
    organization_id = Column(String, nullable=False)

    versions = relationship("TenderVersion", order_by=TenderVersion.version, back_populates="tender")
    bids = relationship("Bid", back_populates="tender")