import uuid
from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship

from ..core.models import BaseModel
from ..db.db import Base


class SolarPanel(Base, BaseModel):
    __tablename__ = "solar_panel"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(JSON, nullable=False)
    max_capacity = Column(Float, nullable=False)
    saved_capacity = Column(Float, nullable=False)
    sold_capacity = Column(Float, nullable=False)
    user = relationship("User", back_populates="orders")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    fee = Column(Float, nullable=False)
