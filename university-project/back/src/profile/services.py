from typing import List, Optional
from pydantic_mongo import ObjectIdField

from pymongo import MongoClient
from fastapi import HTTPException, status
import random
from .models import Profile
from ..auth.models import User
from .schemas import ProfileRes
from ..auth.schemas import ProfileCreate, ProfileOut, ProfileUpdate

from ..db.db import client, db
from bson import ObjectId


class ProfileService:
    """
    Repository class for interacting with the Profile model in the database.

    Attributes:
        client (MongoClient): MongoDB client.
        db_name (str): Name of the MongoDB database.
    """

    def __init__(self):
        self.db = db

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
                {"user_id": str(user["_id"])},
                # {"user_id": user.id, "is_active": True},
                {"$set": {"photo": random_number}},
                return_document=True
            )
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Profile not found with user ID: {user.id}"
                )
            return ProfileRes(photo=profile['photo'], user={"_id": str(user["_id"]), "email": user['email']})
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
        profile = self.db.profiles.find_one({"user_id": str(user["_id"])})
        # TODO Fix this
        # profile = self.db.profiles.find_one({"user_id": user["_id"], "is_active": True})

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile not found with user ID: {str(user['_id'])}"
            )

        block_details = self.db.blocks.find_one({"user_id": str(user["_id"])})
        apartment_no = self.db.apartments.find_one({"_id": ObjectId(block_details['apartment_id'])})['apartment_no']
        return {'photo': profile['photo'], 'user': {"_id": str(user["_id"]), "email": user['email']},
                "area": block_details['area'],
                "apartment_no": apartment_no,
                }

    def create_profile(self, profile_data: ProfileCreate) -> ProfileOut:
        profile_id = ObjectId()
        profile_data_dict = profile_data.dict()
        profile_data_dict["_id"] = profile_id
        self.db.profiles.insert_one(profile_data_dict)
        return ProfileOut(id=str(profile_id), **profile_data_dict)

    def get_profiles(self, skip: int = 0, limit: int = 10) -> List[ProfileOut]:
        profiles = list(self.db.profiles.find().skip(skip).limit(limit))
        for profile in profiles:
            profile["_id"] = str(profile["_id"])
        return profiles

    def get_profile(self, profile_id: str) -> Optional[ProfileOut]:
        profile = self.db.profiles.find_one({"_id": ObjectId(profile_id)})
        if profile:
            profile["_id"] = str(profile["_id"])
            return profile
        return None

    def update_profile(self, profile_id: str, profile_update: ProfileUpdate) -> Optional[ProfileOut]:
        update_data = profile_update.dict(exclude_unset=True)
        result = self.db.profiles.update_one({"_id": ObjectId(profile_id)}, {"$set": update_data})
        if result.modified_count:
            updated_profile = self.db.profiles.find_one({"_id": ObjectId(profile_id)})
            updated_profile["_id"] = str(updated_profile["_id"])
            return updated_profile
        return None

    def delete_profile(self, profile_id: str) -> Optional[ProfileOut]:
        profile = self.db.profiles.find_one({"_id": ObjectId(profile_id)})
        if profile:
            self.db.profiles.delete_one({"_id": ObjectId(profile_id)})
            profile["_id"] = str(profile["_id"])
            return profile
        return None
