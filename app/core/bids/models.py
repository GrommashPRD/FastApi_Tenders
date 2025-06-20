from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime, UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
import enum
from datetime import datetime


class BidStatus(enum.Enum):
    CREATED = "CREATED"
    PUBLISHED = "PUBLISHED"
    CANCELED = "CANCELED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class BidVersion(Base):
    __tablename__ = "bid_version"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    bid_id = Column(UUID(as_uuid=True), ForeignKey('bids.id'), nullable=False)
    version = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    bid = relationship("Bid", back_populates="versions")

class BidFeedback(Base):
    __tablename__ = 'feedback_bid'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bid_id = Column(UUID(as_uuid=True), ForeignKey('bids.id'), nullable=False)
    feedback = Column(String, nullable=False)
    feedback_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    bid = relationship("Bid", back_populates="feedbacks")

class BidDecisionModel(Base):
    __tablename__ = 'bid_decisions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bid_id = Column(UUID, ForeignKey('bids.id'), nullable=False)
    user_id = Column(String, ForeignKey('employee.id'), nullable=False)
    status = Column(Enum(BidStatus))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


    bid = relationship('Bid', back_populates='decisions')
    user = relationship('User', back_populates='decisions')

class Bid(Base):
    __tablename__ = 'bids'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(BidStatus))
    tender_id = Column(UUID, ForeignKey('tenders.id'), nullable=False)
    organization_id = Column(String)
    creator_username = Column(String, nullable=False)
    version = Column(Integer, default=1)
    votes = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    versions = relationship("BidVersion", order_by=BidVersion.version, back_populates="bid")
    tender = relationship("Tender", back_populates="bids")
    feedbacks = relationship("BidFeedback", order_by='BidFeedback.created_at', back_populates="bid")
    decisions = relationship('BidDecisionModel', back_populates='bid')