import enum
import uuid
from typing import List

from pydantic import UUID4, Field, constr
from sqlalchemy import Column, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from sqlalchemy.dialects.postgresql import UUID, JSON

from ..auth.models import User
from ..core.models import BaseModel


class StatusEnum(enum.Enum):
    not_processed = "not_processed"
    processed = "processed"
    cancelled = "cancelled"


class Order(BaseModel):
    """
    Pydantic schema representing an order in the application.
    """
    id: UUID4
    price: float = 0.0
    status: StatusEnum = StatusEnum.not_processed
    volume: float = 0.0
    user: "User"

    class Config:
        orm_mode = True
