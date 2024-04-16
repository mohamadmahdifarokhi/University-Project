import uuid

from pydantic_mongo import ObjectIdField
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from ..core.models import BaseModel

from typing import List

from pydantic import EmailStr, UUID4


class UUIDType(UUID4):
    """
    Custom Pydantic UUID type to handle SQLAlchemy UUID.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """
        Validate the UUID value.

        Args:
            v: The value to validate.

        Returns:
            UUID: The validated UUID value.

        Raises:
            ValueError: If the value is not a valid UUID.
        """
        # Perform validation here
        try:
            return uuid.UUID(str(v))
        except ValueError:
            raise ValueError("Invalid UUID")



class User(BaseModel):
    id: ObjectIdField = None
    email: EmailStr
    password: str
    provider: str
    permissions: List["Permission"] = []
    # TODO badab biyar
    # devices: List["Device"] = []
    # block: Optional["Block"] = None

    class Config:
        orm_mode = True


class OTP(BaseModel):
    id: UUIDType
    otp_code: int
    email: EmailStr
    expired_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    id: UUIDType
    token: str
    email: EmailStr
    expired_at: datetime

    class Config:
        orm_mode = True


class Permission(BaseModel):
    id: UUIDType
    name: str
    description: str

    class Config:
        orm_mode = True

