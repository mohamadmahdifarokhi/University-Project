import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from ..core.models import BaseModel
from ..db.db import Base


class User(Base, BaseModel):
    """
    Represents a user in the system.

    Attributes:
        id (UUID): Unique identifier for the user.
        email (str): Email address associated with the user.
        password (str): password associated with the user.

    Relationships:
        profile (relationship): One-to-one relationship with the Profile model.
        cart (relationship): One-to-one relationship with the Cart model.
        permission_set (relationship): One-to-many relationship with PermissionSet model.
        order (relationship): One-to-one relationship with the Order model.
    """
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    email = Column(EmailType, unique=True, nullable=False, index=True)
    password = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    profile = relationship("Profile", back_populates="user", uselist=False)
    cart = relationship("Cart", back_populates="user", uselist=False)
    permission_set = relationship("PermissionSet", back_populates="user")
    orders = relationship("Order", back_populates="user")

    __table_args__ = (CheckConstraint("CHAR_LENGTH(password) >= 8"),)


class OTP(Base, BaseModel):
    """
    Represents a One-Time Password (OTP) for user authentication.

    Attributes:
        id (UUID): Unique identifier for the OTP record.
        otp_code (int): Numeric code used for authentication.
        email (str): Email address associated with the OTP.
        expired_at (DateTime): Timestamp indicating OTP expiration.
    """
    __tablename__ = "otp"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    otp_code = Column(Integer, nullable=False, unique=True, index=True)
    email = Column(EmailType, nullable=False, unique=True, index=True)
    expired_at = Column(DateTime, nullable=False)

    __table_args__ = (CheckConstraint("otp_code >= 100000 AND otp_code <= 999999"),)


class Token(Base, BaseModel):
    """
    Represents an authentication token.

    Attributes:
        id (UUID): Unique identifier for the token.
        token (str): Authentication token.
        email (str): Email address associated with the token.
        expired_at (DateTime): Timestamp indicating token expiration.
    """
    __tablename__ = "token"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    token = Column(UUID, nullable=False, unique=True, index=True)
    email = Column(EmailType, nullable=False, unique=True, index=True)
    expired_at = Column(DateTime, nullable=False)


class Permission(Base, BaseModel):
    """
    Represents a permission that can be assigned to users.

    Attributes:
        id (UUID): Unique identifier for the permission.
        name (str): Name of the permission.
        description (str): Description of the permission.

    Relationships:
        permission_set (relationship): One-to-many relationship with PermissionSet model.
    """
    __tablename__ = "permission"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)

    permission_set = relationship("PermissionSet", back_populates="permission")


class PermissionSet(Base, BaseModel):
    """
    Represents a set of permissions assigned to a user.

    Attributes:
        id (UUID): Unique identifier for the permission set.

    Relationships:
        user (relationship): Many-to-one relationship with User model.
        permission (relationship): Many-to-one relationship with Permission model.
    """
    __tablename__ = "permission_set"
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="permission_set")

    permission_id = Column(
        UUID(as_uuid=True), ForeignKey("permission.id"), nullable=False
    )
    permission = relationship("Permission", back_populates="permission_set")

    def __str__(self):
        return self.permission.name
