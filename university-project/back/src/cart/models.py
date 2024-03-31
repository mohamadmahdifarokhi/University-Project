import uuid
from sqlalchemy import Column, ForeignKey, Text, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..core.models import BaseModel
from ..db.db import Base
from sqlalchemy_utils import EmailType


class Cart(Base, BaseModel):
    """
    Model class for representing a shopping cart.

    Attributes:
        id (UUID): Primary key for the cart, generated using uuid.uuid4().
        user_id (UUID): Foreign key referencing the associated user ID.
        user (User): Relationship with the User model, representing the owner of the cart.
        cart_items (list[CartItem]): Relationship with the CartItem model, representing items in the cart.
    """
    __tablename__ = "cart"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    user = relationship("User", back_populates="cart")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, unique=True, index=True)
    cart_items = relationship("CartItem", back_populates="cart")

    def __str__(self):
        return self.user.email


class CartItem(Base, BaseModel):
    """
    Model class for representing an item in a shopping cart.

    Attributes:
        id (UUID): Primary key for the CartItem, generated using uuid.uuid4().
        email (str): Email associated with the item (nullable).
        password (str): Password associated with the item (nullable).
        description (str): Description of the item (nullable).
        cart (Cart): Relationship with the Cart model, representing the cart to which the item belongs.
        cart_id (UUID): Foreign key referencing the associated cart ID.
        product (Product): Relationship with the Product model, representing the product associated with the item.
        product_id (UUID): Foreign key referencing the associated product ID.
    """
    __tablename__ = "cart_item"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    email = Column(EmailType, nullable=True)
    password = Column(String, nullable=True)
    description = Column(Text, nullable=True)

    cart = relationship("Cart", back_populates="cart_items")
    cart_id = Column(UUID(as_uuid=True), ForeignKey("cart.id"), nullable=False)

    product = relationship("Product", back_populates="cart_item")
    product_id = Column(UUID(as_uuid=True), ForeignKey("product.id"), nullable=False)

    def __str__(self):
        return f"User: {self.cart.user.email}"
