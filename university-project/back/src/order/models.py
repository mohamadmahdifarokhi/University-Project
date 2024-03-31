import enum
import uuid

from sqlalchemy import Column, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from sqlalchemy.dialects.postgresql import UUID, JSON

from ..core.models import BaseModel
from ..db.db import Base


class StatusEnum(enum.Enum):
    not_processed = "not_processed"
    processed = "processed"
    cancelled = "cancelled"


class Order(Base, BaseModel):
    """
    Model class representing an order entity.

    Attributes:
    - id (UUID): Primary key for the order, generated using UUID.
    - transaction_id (str): Transaction ID for the order.
    - price (float): Total price of the order.
    - discount_price (float): Discounted price of the order.
    - status (StatusEnum): Order status (not_processed, processed, shipped, delivered, cancelled).
    - user_id (UUID): Foreign key for the User model.
    - user (User): Relationship with the User model.
    - order_items (List[OrderItem]): Relationship with the OrderItem model.
    """

    __tablename__ = "order"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    transaction_id = Column(String, nullable=False, unique=True, index=True)
    price = Column(Float, default=0.0, nullable=False)
    discount_price = Column(Float, default=0.0, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.not_processed, nullable=False)

    user = relationship("User", back_populates="orders")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    order_items = relationship("OrderItem", back_populates="order")

    def __str__(self):
        return self.user.email


class OrderItem(Base, BaseModel):
    """
    Model class representing an order item entity.

    Attributes:
    - id (UUID): Primary key for the order item, generated using UUID.
    - name (str): Name of the order item.
    - price (float): Price of the order item.
    - discount_price (float): Discounted price of the order item.
    - email (str): Email associated with the order item.
    - password (str): Password associated with the order item.
    - description (str): Description of the order item.
    - status (StatusEnum): Order item status (not_processed, processed, shipped, delivered, cancelled).
    - order (Order): Relationship with the Order model.
    - orderId (UUID): Foreign key for the Order model.
    - product (Product): Relationship with the Product model.
    - product_id (UUID): Foreign key for the Product model.
    """

    __tablename__ = "orderItem"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(JSON, nullable=False)
    price = Column(Float, default=0.0, nullable=False)
    discount_price = Column(Float, default=0.0, nullable=False)
    email = Column(EmailType, nullable=True)
    password = Column(String, nullable=True)
    description = Column(JSON, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.not_processed, nullable=False)

    order = relationship("Order", back_populates="order_items")
    orderId = Column(UUID(as_uuid=True), ForeignKey("order.id"), nullable=False)

    product = relationship("Product", back_populates="order_items")
    product_id = Column(UUID(as_uuid=True), ForeignKey("product.id"), nullable=False)

    def __str__(self):
        return f"User: {self.order.user.email} - Product: {self.product.name}"
