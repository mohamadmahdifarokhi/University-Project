import uuid
from sqlalchemy import Column, ForeignKey, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..core.models import BaseModel
from ..db.db import Base


class Profile(Base, BaseModel):
    """
    Model representing a user profile in the application.

    Attributes:
        id (UUID): Primary key for the profile, generated using uuid.uuid4().
        photo (int): Number of the profile photo. Should be between 1 and 26.
        user_id (UUID): Foreign key referencing the associated user ID.
        user (User): Relationship with the User model.
    """
    __tablename__ = "profile"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    photo = Column(Integer, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, unique=True, index=True)
    user = relationship("User", back_populates="profile")

    __table_args__ = (
        CheckConstraint('photo >= 1 AND photo <= 26', name='check_valid_photo'),
    )

    def __str__(self):
        return self.user.email
