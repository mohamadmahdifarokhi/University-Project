from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import UUID4, BaseModel, EmailStr, constr, conint

from ..order.models import Order
from ..profile.models import Profile


class Permission(BaseModel):
    id: UUID
    name: str
    description: str

    class Config:
        orm_mode = True


class User(BaseModel):
    id: UUID
    email: EmailStr
    password: str
    provider: str
    profile: Optional["Profile"] = None
    permissions: List["Permission"] = []
    orders: List["Order"] = []

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


# ------------------------------------


class UserReq(BaseModel):
    """
    Request model for user.

    Attributes:
        email (EmailStr): User's email address.
        password (constr): User's password.
    """
    email: EmailStr
    password: constr(min_length=8)


class UserRes(BaseModel):
    """
    Response model for user user.

    Attributes:
        email (EmailStr): User's email address.
    """
    email: EmailStr


class UserUp(BaseModel):
    """
    Update model for user.

    Attributes:
        email (EmailStr): User's email address.
        password (constr): User's password.
    """
    email: EmailStr | None = None
    password: constr(min_length=8) | None = None


class OtpReq(BaseModel):
    """
    Request model for generating OTP.

    Attributes:
        email (EmailStr): User's email address.
    """
    email: EmailStr

    class Config:
        orm_mode = True


class OtpRes(BaseModel):
    """
    Response model for OTP generation.

    Attributes:
        id (UUID4): Unique identifier for the response.
        email (EmailStr): User's email address.
        otp_code (constr): Generated one-time password.
    """
    id: str
    email: EmailStr
    # TODO badan baresh dar
    otp_code: int




class VerifyOtpReq(BaseModel):
    """
    Request model for generating OTP.

    Attributes:
        email (EmailStr): User's email address.
        password (constr): User's password.
        otp_code (constr): Generated one-time password.
    """
    email: EmailStr
    password: constr(min_length=8)
    otp_code: conint(ge=100000, le=999999)
    class Config:
        orm_mode = True

class VerifyCodeReq(BaseModel):
    """
    Request model for generating Auth Code.

    Attributes:
        code (str): User's auth code.
    """
    code: str


class SendEmailReq(BaseModel):
    """
    Request model for generating Auth Code.

    Attributes:
        code (str): User's auth code.
    """
    email: str
    subject: str
    description: str


class TokenReq(BaseModel):
    """
    Request model for generating authentication token.

    Attributes:
        email (EmailStr): User's email address.
    """
    email: EmailStr


class TokenRes(BaseModel):
    """
    Response model for authentication token generation.

    Attributes:
        email (EmailStr): User's email address.
        token (UUID4): Generated authentication token.
    """
    email: EmailStr
    # TODO badan baresh dar
    token: UUID4
    expired_at: datetime


class VerifyTokenReq(BaseModel):
    """
    Request model for generating Token.

    Attributes:
        token (constr): authentication token.
    """
    token: UUID4


class TokenPasswordReq(BaseModel):
    """
        Request model for generating Token.

        Attributes:
            token (UUID4): authentication token.
            password (constr): User's new password.
        """
    token: UUID4
    password: constr(min_length=8)


class PasswordReq(BaseModel):
    """
        Request model for generating Token.

        Attributes:
            password (constr): User's password.
            new_password (constr): User's new password.
        """
    password: constr(min_length=8)
    new_password: constr(min_length=8)
