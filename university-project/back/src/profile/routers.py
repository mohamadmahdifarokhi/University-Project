import time

from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.auth.models import User
from .schemas import ProfileRes
from .services import ProfileService
from src.auth.secures import get_user
from ..db.db import sess_db

router = APIRouter(tags=["Profiles"])


# @router.post("/add")
# def add_profile(
#     req: ProfileReq,
#     user: User = Security(get_current_user),
#     sess: Session = Depends(sess_db),
# ):
#     """
#     Create a new user profile.
#
#     Args:
#         req (ProfileReq): Request body containing profile information.
#         user (User): Current user obtained from authentication.
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         JSONResponse: JSON response containing the created profile or an error message.
#     """
#     profile_dict = req.dict(exclude_unset=True)
#     repo: ProfileService = ProfileService(sess)
#     random_numbers = random.randint(1, 26)
#     profile = Profile(photo=random_numbers, **profile_dict)
#     result = repo.insert_profile(profile)
#
#     if result:
#         return profile
#     else:
#         return JSONResponse(
#             content={"message": "create profile problem encountered"},
#             status_code=500,
#         )


@router.get("", response_model=ProfileRes)
def get_profile_by_user_id(
    user: User = Security(get_user),
):
    """
    Get the current user.

    Args:
        user (User): Current user obtained from authentication.
        sess (Session): SQLAlchemy database session.

    Returns:
        dict: Dictionary containing the user's profile.
    """
    return ProfileService().get_by_user_id(user)


# @router.get("/list")
# def list_all_profile(
#     user: User = Security(get_current_user),
#     sess: Session = Depends(sess_db),
# ):
#     """
#     Get a list of all user profiles.
#
#     Args:
#         user (User): Current user obtained from authentication.
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         List[Profile]: List of profiles.
#     """
#     repo: ProfileService = ProfileService(sess)
#     result = repo.get_all_profile()
#     return result


@router.patch("/update/photo", response_model=ProfileRes)
def change_photo(
    user: User = Security(get_user),
):
    """
    Change the user profile photo.

    Args:
        user (User): Current user obtained from authentication.
        sess (Session): SQLAlchemy database session.

    Returns:
        JSONResponse: JSON response indicating the success or failure of the photo change.
    """
    return ProfileService().change_photo(user)

# @router.patch("/update")
# def update_profile(
#     req: ProfileUpdate,
#     user: User = Security(get_current_user),
#     sess: Session = Depends(sess_db),
# ):
#     """
#     Update the user profile.
#
#     Args:
#         req (ProfileUpdate): Request body containing updated profile information.
#         user (User): Current user obtained from authentication.
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         JSONResponse: JSON response indicating the success or failure of the profile update.
#     """
#     profile_dict = req.dict(exclude_unset=True)
#     repo: ProfileService = ProfileService(sess)
#     resulted = repo.update_profile(user.profiles.id, profile_dict)
#
#     if resulted:
#         return JSONResponse(
#             content={"message": "profile updated successfully"}, status_code=201
#         )
#     else:
#         return JSONResponse(
#             content={"message": "update profile error"}, status_code=500
#         )

# @router.delete("/delete/{id}")
# def delete_profile(
#     id: int,
#     user: User = Security(
#         get_current_user, scopes=["bidder_write", "buyer_write"]
#     ),
#     sess: Session = Depends(sess_db),
# ):
#     """
#     Delete a user profile.
#
#     Args:
#         id (int): ID of the profile to be deleted.
#         user (User): Current user obtained from authentication.
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         JSONResponse: JSON response indicating the success or failure of the profile deletion.
#     """
#     repo: ProfileService = ProfileService(sess)
#     result = repo.delete(id)
