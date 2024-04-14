from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from ..core.models import BaseModel

from typing import List

from pydantic import EmailStr


class User(BaseModel):
    id: UUID
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
    id: UUID
    otp_code: int
    email: EmailStr
    expired_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    id: UUID
    token: str
    email: EmailStr
    expired_at: datetime

    class Config:
        orm_mode = True


class Permission(BaseModel):
    id: UUID
    name: str
    description: str

    class Config:
        orm_mode = True

