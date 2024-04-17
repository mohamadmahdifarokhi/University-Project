from datetime import datetime
from typing import List, Optional, Any, Annotated
from uuid import UUID

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import UUID4, BaseModel, EmailStr, constr, conint, Field
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from ..order.models import Order
from ..profile.models import Profile


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")


class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId:
        if isinstance(v, ObjectId):
            return v

        s = handler(v)
        if ObjectId.is_valid(s):
            return ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        assert source_type is ObjectId
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class Permission(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    name: str | None
    description: str | None

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


class UserBase(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    email: EmailStr
    password: str
    provider: str
    # permissions: List[Permission] = []


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    provider: str | None = None



class UserOut(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    email: EmailStr
    password: str | None
    permissions: List["Permission"] = []

    # provider: str  # Add the provider field

    class Config:
        arbitrary_types_allowed = True


class OTP(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    otp_code: int
    email: EmailStr
    expired_at: datetime

    class Config:
        orm_mode = True


class OTPCreate(BaseModel):
    otp_code: int
    email: EmailStr
    expired_at: datetime

class OTPUpdate(BaseModel):
    otp_code: int | None = None
    email: EmailStr | None = None
    expired_at: datetime | None = None

class OTPOut(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    otp_code: int
    email: EmailStr
    expired_at: datetime

    class Config:
        arbitrary_types_allowed = True




class Token(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    token: str
    email: EmailStr
    expired_at: datetime

    class Config:
        orm_mode = True


class TokenCreate(BaseModel):
    token: str
    email: EmailStr
    expired_at: datetime

class TokenUpdate(BaseModel):
    token: str | None = None
    email: EmailStr | None = None
    expired_at: datetime | None = None

class TokenOut(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    token: str
    email: EmailStr
    expired_at: datetime

    class Config:
        arbitrary_types_allowed = True

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


class PermissionCreate(BaseModel):
    name: str
    description: str

class PermissionUpdate(BaseModel):
    name: str
    description: str

class PermissionOut(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    name: str
    description: str

    class Config:
        arbitrary_types_allowed = True

class ProfileCreate(BaseModel):
    photo: conint(ge=1, le=26)
    user_id: str

class ProfileUpdate(BaseModel):
    photo: Optional[conint(ge=1, le=26)] = None

class ProfileOut(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    photo: int
    user_id: str
    class Config:
        arbitrary_types_allowed = True
