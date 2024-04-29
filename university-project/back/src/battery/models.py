import enum
import uuid

from sqlalchemy import Column, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from sqlalchemy.dialects.postgresql import UUID, JSON

from ..core.models import BaseModel
from ..db.db import Base


class Device(Base, BaseModel):
    __tablename__ = "device"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ac_power_consumption = Column(Float, default=0.0, nullable=False)
    dc_power_consumption = Column(Float, default=0.0, nullable=False)
    user = relationship("User", back_populates="devices")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    def __str__(self):
        return self.name
