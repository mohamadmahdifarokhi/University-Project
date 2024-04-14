from pymongo import MongoClient
from fastapi import HTTPException, status
import random
from .models import Profile
from ..auth.models import User


class ProfileService:
    """
    Repository class for interacting with the Profile model in the database.

    Attributes:
        client (MongoClient): MongoDB client.
        db_name (str): Name of the MongoDB database.
    """

    def __init__(self, client: MongoClient, db_name: str):
        self.client = client
        self.db = self.client[db_name]

    def change_photo(self, user: User) -> dict:
        """
        Change the photo of a user profile in the database.

        Args:
            user (User): User model.

        Returns:
            dict: Updated Profile object.
        """
        try:
            random_number = random.randint(1, 26)
            profile = self.db.profiles.find_one_and_update(
                {"user_id": user.id, "is_active": True},
                {"$set": {"photo": random_number}},
                return_document=True
            )
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Profile not found with user ID: {user.id}"
                )
            return profile
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to change photo: {str(e)}"
            )

    def get_by_user_id(self, user: User) -> dict:
        """
        Retrieve a user profile based on the user ID from the database.

        Args:
            user (User): User model.

        Returns:
            dict: Profile object if found.
        """
        profile = self.db.profiles.find_one({"user_id": user.id, "is_active": True})
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile not found with user ID: {user.id}"
            )
        return profile
