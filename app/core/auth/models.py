from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
import uuid
from app.database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "employee"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())

    decisions = relationship('BidDecisionModel', back_populates='user')
