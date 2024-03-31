import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from ..core.models import BaseModel, S3ImageType
from ..db.db import Base
from ..core.bucket import boto_client
from sqlalchemy.dialects.postgresql import UUID, JSON


class Category(Base, BaseModel):
    """
    SQLAlchemy model for Category.

    Inherits from Base and BaseModel.

    Attributes:
        id (UUID): The unique identifier for the category.
        name (JSON): The name of the category.
        photo (S3ImageType): The S3 image link associated with the category.
        parent_id (UUID): The unique identifier of the parent category, if any.
        parent (relationship): Relationship with the parent category.
        products (relationship): Relationship with the associated Product model.
    """
    __tablename__ = "category"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(JSON, nullable=False)

    photo = Column(S3ImageType(storage=boto_client), nullable=False, unique=True, index=True)

    parent = relationship("Category", remote_side=[id], backref="children")
    parent_id = Column(UUID(as_uuid=True), ForeignKey("category.id"), nullable=True)

    products = relationship("Product", back_populates="category")

    def __str__(self):
        return str(self.name)

