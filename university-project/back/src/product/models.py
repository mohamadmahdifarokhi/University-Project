import uuid
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSON

from ..core.bucket import boto_client
from ..core.models import BaseModel, S3ImageType
from ..db.db import Base


class Product(Base, BaseModel):
    """
    Model class representing a product entity.

    Attributes:
    - id (UUID): Primary key for the product, generated using UUID.
    - name (str): Name of the product.
    - slug (str): Unique slug for the product, used for indexing.
    - photo (str): Path or URL to the product photo.
    - description (str): Text description of the product.
    - price (float): Regular price of the product.
    - discount_price (float): Discounted price of the product.
    - count (int): Quantity of the product available in stock.
    - sold (int): Quantity of the product sold.
    - category (Category): Relationship with the Category model.
    - category_id (UUID): Foreign key for the Category model.
    - cart_item (CartItem): Relationship with the CartItem model.
    - orderItem (OrderItem): Relationship with the OrderItem model.
    """

    __tablename__ = "product"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(JSON, nullable=False)
    slug = Column(String, nullable=False, unique=True, index=True)
    photo = Column(S3ImageType(storage=boto_client), nullable=False, unique=True, index=True)
    background = Column(S3ImageType(storage=boto_client), nullable=False, unique=True, index=True)
    logo = Column(S3ImageType(storage=boto_client), nullable=False, unique=True, index=True)
    
    description = Column(JSON, nullable=False)
    price = Column(Float, default=10000.0, nullable=False)
    discount_price = Column(Float, default=0.0, nullable=False)
    count = Column(Integer, default=1, nullable=False)
    sold = Column(Integer, default=0, nullable=False)


