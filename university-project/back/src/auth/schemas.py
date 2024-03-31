from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr, constr, conint


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


class OtpRes(BaseModel):
    """
    Response model for OTP generation.

    Attributes:
        id (UUID4): Unique identifier for the response.
        email (EmailStr): User's email address.
        otp_code (constr): Generated one-time password.
    """
    id: UUID4
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

# class PermissionReq(BaseModel):
#     """
#     Request model for creating a new permission.
#
#     Attributes:
#         name (str): Name of the permission.
#         description (str): Description of the permission.
#     """
#     name: str
#     description: str


# class PermissionRes(BaseModelResponse):
#     """
#     Response model for permission creation.
#
#     Attributes:
#         id (UUID4): Unique identifier for the permission.
#     """
#     id: UUID4


# class PermissionSetReq(BaseModel):
#     """
#     Request model for creating a new permission set.
#
#     Attributes:
#         user_id (UUID4): Unique identifier for the user.
#         permission_id (UUID4): Unique identifier for the permission.
#     """
#     user_id: UUID4
#     permission_id: UUID4


# class PermissionSetRes(BaseModelResponse):
#     """
#     Response model for permission set creation.
#
#     Attributes:
#         id (UUID4): Unique identifier for the permission set.
#     """
#     id: UUID4


# class PermissionSetUp(BaseModel):
#     """
#     Request model for updating a new permission set.
#
#     Attributes:
#         user_id (UUID4): Unique identifier for the user.
#         permission_id (UUID4): Unique identifier for the permission.
#     """
#     user_id: UUID4 | None = None
#     permission_id: UUID4 | None = None
