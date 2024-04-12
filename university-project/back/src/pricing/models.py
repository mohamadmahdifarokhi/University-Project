import enum
import uuid

from sqlalchemy import Column, Enum, Float, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from sqlalchemy.dialects.postgresql import UUID, JSON

from ..core.models import BaseModel
from ..db.db import Base


class Pricing(Base, BaseModel):
    __tablename__ = "pricing"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    device = relationship("Device", back_populates="pricing")
    device_id = Column(UUID(as_uuid=True), ForeignKey("device.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    price = Column(Float, default=10000.0, nullable=False)
    peak_time_price = Column(Float, default=10000.0, nullable=False)

    def __str__(self):
        return self.price
