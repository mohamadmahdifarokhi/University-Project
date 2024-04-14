import uuid

from pydantic import conint, Field, UUID4
from sqlalchemy import Column, ForeignKey, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..auth.models import User
from ..core.models import BaseModel
from ..db.db import Base


class Profile(BaseModel):
    """
    Pydantic schema representing a user profile in the application.
    """
    id: UUID4 = Field(default_factory=uuid.uuid4, alias="id")
    photo: conint(ge=1, le=26)
    user: 'User'

    class Config:
        orm_mode = True
