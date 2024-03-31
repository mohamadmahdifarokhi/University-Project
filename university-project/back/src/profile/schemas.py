from pydantic import BaseModel

from src.auth.schemas import UserRes


# class ProfileReq(BaseModel):
#     """
#     Pydantic model for creating a new user profile.
#
#     Attributes:
#         name (str): Name associated with the profile.
#         user_id (UUID4): UUID4 representing the user associated with the profile.
#     """
#     user_id: UUID4


class ProfileRes(BaseModel):
    """
    Pydantic model for the response containing user profile information.

    Attributes:
        photo (int): Integer representing the profile photo.
        user (UserRes): UserRes model representing the associated user.
    """
    photo: int
    user: UserRes

# class ProfileUpdate(BaseModel):
#     """
#     Pydantic model for updating a user profile.
#
#     Attributes:
#         name (str): Updated name for the profile.
#         photo (str): Updated photo URL or file path for the profile.
#         user_id (UUID4): Updated UUID4 representing the user associated with the profile.
#     """
#     name: str | None = None
#     photo: str | None = None
#     user_id: UUID4 | None = None
