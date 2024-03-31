import random
from typing import Type

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .models import Profile
from ..auth.models import User


class ProfileService:
    """
    Repository class for interacting with the Profile model in the database.

    Attributes:
        sess (Session): SQLAlchemy database session.
    """

    def __init__(self, sess: Session):
        self.sess: Session = sess

    # def insert(self, entity) -> bool:
    #     """
    #     Insert a new entity into the database.
    #
    #     Args:
    #         entity: The entity to be inserted.
    #
    #     Returns:
    #         bool: True if the operation is successful, False otherwise.
    #     """
    #     try:
    #         random_numbers = random.randint(1, 26)
    #         entity.photo = random_numbers
    #         self.sess.add(entity)
    #         self._commit_or_rollback()
    #         logger.info(f"Inserted {self.model.__name__} with ID: {entity.id}")
    #     except Exception as e:
    #         logger.error(f"Insert operation failed: {e}")
    #         return False
    #     return True

    def change_photo(self, user: User) -> Type[Profile]:
        """
        Change the photo of a user profile in the database.

        Args:
            user (User): User model.

        Returns:
            Profile: Updated Profile object.
        """
        random_number = random.randint(1, 26)
        profile = self.sess.query(Profile).filter_by(id=user.profile.id, is_active=True).first()
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile not found with ID: {user.profile.id}"
            )
        profile.photo = random_number
        self.sess.commit()
        return profile

    def get_by_user_id(self, user: User) -> Type[Profile]:
        """
        Retrieve a user profile based on the user ID from the database.

        Args:
            user (User): User model.

        Returns:
            Profile: Profile object if found.
        """
        profile = self.sess.query(Profile).filter_by(user_id=user.id, is_active=True).first()
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile not found with user ID: {user.id}"
            )
        return profile
