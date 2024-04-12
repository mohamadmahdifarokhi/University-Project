import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from ..core.models import BaseModel
from ..db.db import Base


class Block(Base, BaseModel):
    __tablename__ = "block"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(JSON, nullable=False)
    user = relationship("User", back_populates="block")
