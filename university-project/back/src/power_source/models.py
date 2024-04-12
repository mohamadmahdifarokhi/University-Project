import enum
import uuid

from sqlalchemy import Column, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from sqlalchemy.dialects.postgresql import UUID, JSON

from ..core.models import BaseModel
from ..db.db import Base




class PowerSource(Base, BaseModel):

    __tablename__ = "power_source"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    capacity = Column(Float, default=0.0, nullable=False)
    remain_capacity = Column(Float, default=0.0, nullable=False)

    def __str__(self):
        return self.capacity
