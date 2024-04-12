import enum
import uuid

from sqlalchemy import Column, Enum, Float, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from sqlalchemy.dialects.postgresql import UUID, JSON

from ..core.models import BaseModel
from ..db.db import Base


class PowerRecords(Base, BaseModel):
    __tablename__ = "power_records"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    power_consumed = Column(Float, nullable=True)
    type_consumed = Column(Float, nullable=True)

    def __str__(self):
        return self.power_consumed
