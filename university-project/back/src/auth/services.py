from uuid import UUID, uuid4
from datetime import timedelta, datetime
import random
from typing import Optional, Type, List, Tuple, Any

import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import User, OTP, Token, Permission, PermissionSet
from .schemas import TokenReq, OtpReq
from .secures import authenticate, create_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash, \
    REFRESH_TOKEN_EXPIRE_DAYS
from ..cart.models import Cart
from ..core.utils import EmailSender
from ..logger import logger
from ..profile.models import Profile


class UserService:
    """
    Service class for handling User-related operations.

    Args:
        sess (Session): The SQLAlchemy database session.
    """

    def __init__(self, sess: Session):
        """
        Initialize the UserService.

        Args:
            sess (Session): The SQLAlchemy database session.
        """
        self.sess: Session = sess

    def insert(self, req, admin=False) -> User:
        """
        Insert a new user entity into the database.

        Args:
            req: The user entity to be inserted.
            admin (bool): Indicates whether the user should have admin privileges.

        Returns:
            User: The inserted user entity.

        Raises:
            HTTPException: If the operation fails, such as if the email already exists.
        """
        try:
            if self.sess.query(User).filter_by(email=req.email).first():
                raise HTTPException(status_code=400, detail="Email already exists")

            otp_service = OTPService(self.sess)
            otp = otp_service.verify(email=req.email, otp_code=req.otp_code)
            self.sess.delete(otp)
            print("aasd")

            password = get_password_hash(req.password)
            user = User(email=req.email, password=password)
            self.sess.add(user)
            print("a")
            permission_service = PermissionService(self.sess)
            user_permission = permission_service.get_by_name("user")
            user_permission_set = PermissionSet(user=user, permission_id=user_permission.id)
            self.sess.add(user_permission_set)
            print("asdasd")

            if admin:
                admin_permission = permission_service.get_by_name("admin")
                admin_permission_set = PermissionSet(user=user, permission_id=admin_permission.id)
                self.sess.add(admin_permission_set)

            random_numbers = random.randint(1, 26)
            profile = Profile(user=user, photo=random_numbers)
            self.sess.add(profile)
            print("asasa")

            cart = Cart(user=user)
            self.sess.add(cart)
            print("wdwdwd")

            self.sess.commit()
            a_token, _, expires_delta_a, a_scopes = self.create_token(
                user.email, user.password, auth=False
            )
            print("dvdvdf")
            print(a_token)

            headers = {'content-type': "application/json", 'access-token': f'Bearer {a_token}'}
            payload = {
                'userId': str(user.id)
            }
            response = requests.post('http://127.0.0.1:8001/shared-account/', json=payload, headers=headers)
            print(response.json())
            if response.status_code != 201:
                raise HTTPException(status_code=400, detail="Failed to create shared account for the user.")
            print("dvaaaadvdf")

            logger.info(f"Inserted User with ID: {user.id}, Email: {user.email}")
            logger.info(f"Inserted Profile with ID: {profile.id}, User ID: {user.id}")
            logger.info(f"Inserted Cart with ID: {cart.id}, User ID: {user.id}")

            return user

        except HTTPException:
            raise
        except Exception as e:
            self.sess.rollback()
            logger.error(f"Insert operation failed: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_by_email(self, email: str) -> Type[User]:
        """
        Get a user by email.

        Args:
            email (str): The email to search for.

        Returns:
            User: The user entity if found, otherwise None.

        Raises:
            HTTPException: If the user is not found or an internal server error occurs.
        """
        try:
            user = self.sess.query(User).filter_by(email=email).first()
            if not user:
                raise HTTPException(status_code=404, detail=f"User with email '{email}' not found")
            return user
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update(self, user_id: UUID, req) -> User:
        """
        Update a user entity in the database.

        Args:
            user_id (UUID): The ID of the user entity to be updated.
            req: The details to be updated.

        Returns:
            User: The updated user entity.

        Raises:
            HTTPException: If the update operation fails.
        """
        try:
            user = self.sess.query(User).get(user_id)

            if req.email and req.email != user.email:
                if self.sess.query(User).filter_by(email=req.email).first():
                    raise HTTPException(status_code=400, detail="Email already exists")

            if req.password:
                req.password = get_password_hash(req.password)

            for field, value in req.dict(exclude_unset=True).items():
                setattr(user, field, value)

            self.sess.commit()
            logger.info(f"Updated User with ID: {user_id}, Email: {user.email}")
        except HTTPException:
            raise
        except Exception as e:
            self.sess.rollback()
            logger.error(f"Update operation failed: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update the User record"
            )
        return user

    def create_token(self, email, password, token_type="access", auth=False) -> tuple[str, Any, timedelta, list[Any]]:
        """
        Create a token for authentication.

        Args:
            email (str): The user's email.
            password (str): The user's password.
            token_type (str): The type of token to create.
            auth (bool): The user's auth.

        Returns:
            tuple[str, UUID, timedelta]: The token, user ID, and expiration time.

        Raises:
            HTTPException: If the token creation fails.
        """
        try:
            user = self.get_by_email(email)

            if auth and not authenticate(password, user):
                raise HTTPException(
                    status_code=400, detail="Incorrect credentials")

            scopes = PermissionSetService(self.sess).get_by_user_id(user.id)

            expires_delta = (
                timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                if token_type == "access"
                else timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            )
            a = [scope.permission.name for scope in scopes]
            print(a, "qweqweqwe")
            token = create_token(
                data={"sub": str(user.id), "scopes": [scope.permission.name for scope in scopes]},
                expires_delta=expires_delta,
            )
            print(token)
            logger.info(f"Token created for User with ID: {user.id}, Email: {user.email}")
            return token, user.id, expires_delta, [scope.permission.name for scope in scopes]

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating token: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")


class OTPService:
    """
    Service class for OTP (One-Time Password) operations.

    Args:
        sess (Session): The SQLAlchemy database session.
    """

    def __init__(self, sess: Session):
        """
        Initialize the OTPService.

        Args:
            sess (Session): The SQLAlchemy database session.
        """
        self.sess: Session = sess

    def insert(self, req: OtpReq) -> OTP:
        """
        Generate a new OTP (One-Time Password) and store it in the database.

        Args:
            req (OtpReq): The request containing the email associated with the OTP.

        Returns:
            OTP: The generated OTP.

        Raises:
            HTTPException: If OTP has already been sent or an internal server error occurs.
        """
        try:
            existing_otp = self.sess.query(OTP).filter_by(email=req.email).first()
            if existing_otp:
                raise HTTPException(status_code=409, detail='OTP has already been sent')

            if self.sess.query(User).filter_by(email=req.email).first():
                raise HTTPException(status_code=400, detail="Email already exists")

            otp_code = random.randint(100000, 999999)
            expired_at = datetime.utcnow() + timedelta(minutes=3)
            otp = OTP(otp_code=otp_code,
                      email=req.email,
                      expired_at=expired_at)
            EmailSender().send_otp_email(req.email, otp_code)
            self.sess.add(otp)
            self.sess.commit()

            logger.info(f"Generated OTP for email: {req.email}, OTP Code: {otp_code}")
            return otp

        except HTTPException:
            raise

        except Exception as e:
            self.sess.rollback()
            logger.error(f"Error inserting OTP: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def verify(self, email: str, otp_code: int) -> Type[OTP]:
        """
        Verify if the provided OTP (One-Time Password) is valid.

        Args:
            email (str): The email associated with the OTP.
            otp_code (int): The OTP code to be verified.

        Returns:
            OTP: The OTP record if the OTP is valid.

        Raises:
            HTTPException: If the OTP is invalid or an internal server error occurs.
        """
        try:
            otp = self.sess.query(OTP).filter_by(email=email).first()
            if otp and otp.otp_code == otp_code:
                logger.info(f"Verified OTP for email: {email}")
                return otp
            raise HTTPException(status_code=400, detail="Invalid OTP code")

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error verifying OTP: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def cleanup_expired_otp(self):
        """
        Cleanup expired OTP (One-Time Password) records from the database.
        """
        try:
            expired_otps = self.sess.query(OTP).filter_by(
                expired_at=lambda expired_at: expired_at <= datetime.utcnow()).all()
            for otp in expired_otps:
                self.sess.delete(otp)
            self.sess.commit()

            logger.info("Cleaned up expired OTP records")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error cleaning up expired OTP: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")


class TokenService:
    """
    Service class for Token operations.

    Args:
        sess (Session): The SQLAlchemy database session.
    """

    def __init__(self, sess: Session):
        """
        Initialize the TokenService.

        Args:
            sess (Session): The SQLAlchemy database session.
        """
        self.sess: Session = sess

    def insert(self, req: TokenReq) -> Token:
        """
        Generate a new token and store it in the database.

        Args:
            req (TokenReq): The request containing the email associated with the token.

        Returns:
            Token: The generated token.

        Raises:
            HTTPException: If the user is not found or if there's an issue generating and storing the token.
        """
        try:
            UserService(self.sess).get_by_email(req.email)
            existing_token = self.sess.query(Token).filter_by(email=req.email).first()

            if existing_token:
                raise HTTPException(
                    status_code=409,
                    detail='A token for this email already exists'
                )

            while True:
                token_value = str(uuid4())
                existing_token = self.sess.query(Token).filter_by(token=token_value).first()

                if not existing_token:
                    try:
                        expired_at = datetime.utcnow() + timedelta(hours=1)
                        token = Token(token=token_value, email=req.email, expired_at=expired_at)
                        EmailSender().send_token_email(req.email, token)
                        self.sess.add(token)
                        self.sess.commit()
                        logger.info(f"Generated and stored token for email: {req.email}")
                        return token
                    except Exception as e:
                        self.sess.rollback()
                        logger.error(f"Failed to generate and store token: {e}")
                        raise HTTPException(
                            status_code=500,
                            detail="Failed to generate and store token"
                        )

        except HTTPException:
            raise

        except Exception as e:
            self.sess.rollback()
            logger.error(f"Error inserting token: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def verify_token(self, token_value: UUID) -> Type[Token] | None:
        """
        Verify if the provided token is valid.

        Args:
            token_value (UUID): The token to be verified.

        Returns:
            Token: The Token record if the token is valid.

        Raises:
            HTTPException: If the token is invalid or has expired.
        """
        try:
            token = self.sess.query(Token).filter_by(token=token_value).first()
            if token and token.expired_at >= datetime.utcnow():
                logger.info(f"Verified token for email: {token.email}")
                return token
            raise HTTPException(status_code=400, detail="Invalid token or token has expired")

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def cleanup_expired_tokens(self):
        """
        Cleanup expired token records from the database.
        """
        try:
            expired_tokens = (
                self.sess.query(Token).filter_by(expired_at=lambda expired_at: expired_at < datetime.utcnow())
                .all())
            for token in expired_tokens:
                self.sess.delete(token)
            self.sess.commit()
            logger.info("Cleaned up expired token records")

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error cleaning up expired tokens: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_by_token(self, token_value: UUID) -> Type[Token]:
        """
        Retrieve a token record by its token value.

        Args:
            token_value (UUID): The token value.

        Returns:
            Token: The Token record if found.

        Raises:
            HTTPException: If the token is not found or an internal server error occurs.
        """
        try:
            token = self.sess.query(Token).filter_by(token=token_value).first()
            if token:
                logger.info(f"Retrieved token for email: {token.email}")
                return token
            raise HTTPException(status_code=404, detail=f"Token with value '{token_value}' not found")

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error retrieving token by token value: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")


class PermissionService:
    """
    Service class for handling Permission-related operations.

    Args:
        sess (Session): The SQLAlchemy database session.
    """

    def __init__(self, sess: Session):
        """
        Initialize the PermissionService.

        Args:
            sess (Session): The SQLAlchemy database session.
        """
        self.sess: Session = sess

    #     super().__init__(sess, Permission)

    # def insert(self, req: dict) -> Permission:
    #     """
    #     Insert a new permission into the database.
    #
    #     Args:
    #         req (dict): The request body containing the permission details.
    #
    #     Returns:
    #         Permission: The inserted Permission object.
    #     """
    #     name = req.get("name")
    #     existing_permission = self.get_by_name(name)
    #     if existing_permission:
    #         raise HTTPException(
    #             status_code=409,
    #             detail=f"Permission with name '{name}' already exists.")
    #
    #     try:
    #         permission = Permission(name=name, description=req.get("description"))
    #         self.sess.add(permission)
    #         self._commit_or_rollback()
    #         return permission
    #     except Exception as e:
    #         logger.error(f"Insert operation failed: {e}")
    #         raise HTTPException(
    #             status_code=500,
    #             detail="Failed to insert the permission.")

    def get_by_name(self, permission_name: str) -> Type[Permission]:
        """
        Get a permission by its name.

        Args:
            permission_name (str): The name of the permission.

        Returns:
            Optional[Permission]: The Permission object if found, otherwise None.

        Raises:
            HTTPException: If the permission is not found or if there is an error in the database operation.
        """
        try:
            permission = (
                self.sess.query(Permission)
                .filter_by(name=permission_name)
                .first()
            )
            if permission:
                logger.info(f"Retrieved permission by name: {permission_name}")
                return permission
            raise HTTPException(status_code=404, detail=f"Permission with name '{permission_name}' not found")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving permission by name: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    # Add other methods if needed...
    # def update(self, permission_id: UUID, details: PermissionReq):
    #     """
    #     Update a permission in the database.
    #
    #     Args:
    #         permission_id (UUID): The ID of the permission to be updated.
    #         details (dict): The request body containing the details to be updated.
    #
    #     Returns:
    #         Permission: The updated Permission object.
    #     """
    #     name = details.get("name")
    #     existing_permission = self.get_by_name(name)
    #     if existing_permission and existing_permission.id != permission_id:
    #         raise HTTPException(
    #             status_code=409,
    #             detail=f"Permission with name '{name}' already exists."
    #         )
    #
    #     try:
    #         permission = (
    #             self.sess.query(Permission)
    #             .filter_by(id=permission_id)
    #             .update(details.__dict__)
    #         )
    #         self._commit_or_rollback()
    #         logger.info(f"Updated {self.model.__name__} with ID: {permission_id}")
    #         return permission
    #     except Exception as e:
    #         logger.error(f"Update operation failed: {e}")
    #         raise HTTPException(
    #             status_code=500,
    #             detail="Failed to update the permission.")

    # def has_permission(self, user_id: int, permission_id: int) -> bool:
    #     """
    #     Check if a user has a specific permission.
    #
    #     Args:
    #         user_id (int): The ID of the user.
    #         permission_id (int): The ID of the permission.
    #
    #     Returns:
    #         bool: True if the user has the permission, False otherwise.
    #     """
    #     permission_set = (
    #         self.sess.query(PermissionSet)
    #         .filter_by(user_id=user_id, permission_id=permission_id)
    #         .one_or_none()
    #     )
    #     return permission_set is not None


class PermissionSetService:
    """
    Service class for handling PermissionSet-related operations.

    Args:
        sess (Session): The SQLAlchemy database session.
    """

    def __init__(self, sess: Session):
        """
        Initialize the PermissionSetService.

        Args:
            sess (Session): The SQLAlchemy database session.
        """
        self.sess: Session = sess

    # def insert(self, req: dict) -> PermissionSet:
    #     """
    #     Insert a new PermissionSet into the database.
    #
    #     Args:
    #         req (dict): The request body containing the user_id and permission_id.
    #
    #     Returns:
    #         PermissionSet: The inserted PermissionSet object.
    #     """
    #     user_id = req.get("user_id")
    #     permission_id = req.get("permission_id")
    #
    #     # Check if the provided permission_id is valid
    #     self._validate_permission_id(permission_id)
    #
    #     existing_permission_set = self.sess.query(PermissionSet).filter_by(user_id=user_id).first()
    #     if existing_permission_set:
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT,
    #             detail=f"PermissionSet for user with ID {user_id} already exists.")
    #
    #     try:
    #         permission_set = PermissionSet(user_id=user_id, permission_id=permission_id)
    #         self.sess.add(permission_set)
    #         self._commit_or_rollback()
    #         return permission_set
    #     except Exception as e:
    #         logger.error(f"Insert operation failed: {e}")
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail="Failed to insert the PermissionSet.")

    def get_by_user_id(self, user_id: int) -> List[Type[PermissionSet]]:
        """
        Get all PermissionSet records associated with a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            List[PermissionSet]: A list of PermissionSet records.

        Raises:
            HTTPException: If there is an error in the database operation or if no PermissionSet records are found.
        """
        try:
            permission_set = self.sess.query(PermissionSet).filter_by(user_id=user_id).all()
            if permission_set:
                logger.info(f"Retrieved Permission Set by user ID: {user_id}")
                return permission_set
            raise HTTPException(status_code=404, detail=f"No Permission Set found for user with ID '{user_id}'")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving Permission Set by user ID: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    # def update(self, permission_set_id: UUID, details: PermissionSetUp):
    #     """
    #     Update a PermissionSet in the database.
    #
    #     Args:
    #         permission_set_id (UUID): The ID of the PermissionSet to be updated.
    #         details (dict): The request body containing the user_id and permission_id.
    #
    #     Returns:
    #         PermissionSet: The updated PermissionSet object.
    #     """
    #     user_id = details.get("user_id")
    #     permission_id = details.get("permission_id")
    #
    #     self._validate_permission_id(permission_id)
    #
    #     existing_permission_set = self.sess.query(PermissionSet).filter_by(user_id=user_id).first()
    #     if existing_permission_set and existing_permission_set.id != permission_set_id:
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT,
    #             detail=f"PermissionSet for user with ID {user_id} already exists.")
    #
    #     try:
    #         permission_set = (
    #             self.sess.query(PermissionSet)
    #             .filter_by(id=permission_set_id)
    #             .update(details.__dict__)
    #         )
    #         self._commit_or_rollback()
    #         logger.info(f"Updated {self.model.__name__} with ID: {permission_set_id}")
    #         return permission_set
    #     except Exception as e:
    #         logger.error(f"Update operation failed: {e}")
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail="Failed to update the PermissionSet.")

    # def _validate_permission_id(self, permission_id: int):
    #     """
    #     Validate if the provided permission_id is valid.
    #
    #     Args:
    #         permission_id (int): The ID of the permission.
    #
    #     Raises:
    #         HTTPException: If the permission_id is not valid.
    #     """
    #     if not self.sess.query(Permission).filter_by(id=permission_id).first():
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail=f"Invalid permission_id: {permission_id}. Permission not found.")
