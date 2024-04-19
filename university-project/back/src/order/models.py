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
from ..db.db import Base


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


# class Order(Base, BaseModel):
#     """
#     Model class representing an order entity.
#
#     Attributes:
#     - id (UUID): Primary key for the order, generated using UUID.
#     - transaction_id (str): Transaction ID for the order.
#     - price (float): Total price of the order.
#     - discount_price (float): Discounted price of the order.
#     - status (StatusEnum): Order status (not_processed, processed, shipped, delivered, cancelled).
#     - user_id (UUID): Foreign key for the User model.
#     - user (User): Relationship with the User model.
#     - order_items (List[OrderItem]): Relationship with the OrderItem model.
#     """
#
#     __tablename__ = "order"
#
#     id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
#     price = Column(Float, default=0.0, nullable=False)
#     status = Column(Enum(StatusEnum), default=StatusEnum.not_processed, nullable=False)
#     volume = Column(Float, default=0.0, nullable=False)
#     user = relationship("User", back_populates="orders")
#     user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
#
#     def __str__(self):
#         return self.user.email
