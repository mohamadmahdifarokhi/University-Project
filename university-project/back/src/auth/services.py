from uuid import UUID, uuid4
from datetime import timedelta, datetime
import random
from typing import Type, List, Optional

from bson import ObjectId
from fastapi import HTTPException
from ..db.db import client, db

from .models import User, Permission, OTP, Token
from .schemas import TokenReq, OtpReq, OtpRes, UserOut, UserUpdate, UserCreate, Permission, OTPCreate, OTPUpdate, \
    OTPOut, TokenCreate, TokenUpdate, TokenOut, PermissionCreate, PermissionOut, PermissionUpdate
from .secures import authenticate, create_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash, \
    REFRESH_TOKEN_EXPIRE_DAYS
from ..core.utils import EmailSender
from ..logger import logger


class UserService:

    def __init__(self):
        self.db = db  # Change 'your_database_name' to your actual MongoDB database name

    def create_user(self, user: UserCreate) -> UserOut:
        user_data = user.dict()
        user_id = str(ObjectId())
        user_data["_id"] = user_id
        user_data["permissions"] = [Permission(id=str(permission["_id"]), **permission) for permission in
                               user.get("permissions", [])]
        self.db.users.insert_one(user_data)
        return user_data

    def get_users(self, skip: int = 0, limit: int = 10) -> List[UserOut]:
        users = list(self.db.users.find().skip(skip).limit(limit))
        for user in users:
            user["_id"] = str(user["_id"])
            user["permissions"] = [Permission(id=str(permission["_id"]), **permission) for permission in user.get("permissions", [])]
        return users

    def get_user(self, user_id: str) -> Optional[UserOut]:
        user = self.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            user["permissions"] = [Permission(id=str(permission["_id"]), **permission) for permission in user.get("permissions", [])]
            return user
        return None

    def update_user(self, user_id: str, user_update: UserUpdate) -> str | None:
        update_data = user_update.dict(exclude_unset=True)
        result = self.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        print(result)
        if result.modified_count:
            updated_user = self.db.users.find_one({"_id": ObjectId(user_id)})
            updated_user["_id"] = str(updated_user["_id"])
            updated_user["permissions"] = [Permission(id=str(permission["_id"]), **permission) for permission in updated_user.get("permissions", [])]
            return 'success'
        return None

    def delete_user(self, user_id: str) -> Optional[UserOut]:
        user = self.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            self.db.users.delete_one({"_id": ObjectId(user_id)})
            user["_id"] = str(user["_id"])
            user["permissions"] = [Permission(id=str(permission["_id"]), **permission) for permission in user.get("permissions", [])]
            return user
        return None

    def insert(self, req, admin=False):
        req = dict(req)
        try:
            # Check if email already exists
            if self.db.users.find_one({"email": req['email']}):
                raise HTTPException(status_code=400, detail=f"Email already exists")
            otp_service = OTPService()  # Change to pymongo equivalent if necessary
            otp = otp_service.verify(email=req['email'], otp_code=req['otp_code'])
            self.db.otps.delete_one({"_id": ObjectId(otp["_id"])})
            password = get_password_hash(req['password'])
            permission_service = PermissionService()  # Change to pymongo equivalent if necessary
            user_permissions = [permission_service.get_by_name("user")]
            if admin:
                admin_permission = permission_service.get_by_name("admin")
                user_permissions.append(admin_permission)
            user_data = {"email": req['email'], "password": password, "permissions": user_permissions}
            print(user_permissions)
            user = self.db.users.insert_one(user_data)
            user_id = user.inserted_id

            random_numbers = random.randint(1, 26)
            profile_data = {"user_id": str(user_id), "photo": random_numbers}
            profile = self.db.profiles.insert_one(profile_data)
            return {"_id": str(user_id), "email": req['email']}
        except HTTPException:
            raise
        except Exception as e:
            print(e)
            # Logging and error handling
            raise Exception("Insert operation failed: " + str(e))

    def get_by_email(self, email: str) -> Type[User]:
        try:
            user = self.db.users.find_one({"email": email})
            if not user:
                raise HTTPException(status_code=404, detail=f"User with email '{email}' not found")
            return user
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update(self, user_id: str, req):
        try:
            # Find user by ID
            user = self.db.users.find_one({"_id": ObjectId(user_id)})

            if not user:
                raise HTTPException(status_code=404, detail=f"User with ID '{user_id}' not found")

            if req.email and req.email != user['email']:
                if self.db.users.find_one({"email": req.email}):
                    raise HTTPException(status_code=400, detail="Email already exists")

            if req.password:
                req.password = get_password_hash(req.password)

            # Update user data
            update_data = {"$set": req.dict(exclude_unset=True)}
            self.db.users.update_one({"_id": ObjectId(user_id)}, update_data)

            logger.info(f"Updated User with ID: {user_id}, Email: {user['email']}")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Update operation failed: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update the User record"
            )
        return self.db.users.find_one({"_id": ObjectId(user_id)})

    def create_token(self, email, password, token_type="access", auth=False):
        try:
            user = self.get_by_email(email)
            print("aaaaaaaadasd")
            if auth and not authenticate(password, user):
                raise HTTPException(
                    status_code=400, detail="Incorrect credentials")
            print("asdasd")
            print(user)

            # Assuming PermissionSetService is a similar MongoDB service
            # scopes = PermissionSetService(self.db).get_by_user_id(user['_id'])

            expires_delta = (
                timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                if token_type == "access"
                else timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            )

            token = create_token(
                data={"sub": str(user['_id']), "scopes": [permission['name'] for permission in user['permissions']]},
                expires_delta=expires_delta,
            )
            logger.info(f"Token created for User with ID: {user['_id']}, Email: {user['email']}")
            return token, str(user['_id']), expires_delta, [permission['name'] for permission in user['permissions']]

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating token: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")


class OTPService:

    def __init__(self):
        self.client = client
        self.db = db  # Change 'your_database_name' to your actual MongoDB database name

    def insert(self, req: OtpReq):
        req = dict(req)
        try:
            existing_otp = self.db.otps.find_one({"email": req['email']})
            if existing_otp:
                raise HTTPException(status_code=409, detail='OTP has already been sent')
            print("aaaaaaaaaa")
            if self.db.users.find_one({"email": req['email']}):
                raise HTTPException(status_code=400, detail="Email already exists")

            otp_code = random.randint(100000, 999999)
            expired_at = datetime.utcnow() + timedelta(minutes=3)
            otp_data = {
                "otp_code": otp_code,
                "email": req['email'],
                "expired_at": expired_at
            }
            result = self.db.otps.insert_one(otp_data)
            inserted_id = str(result.inserted_id)
            print("awdww")
            print(otp_data)
            logger.info(f"Generated OTP for email: {req['email']}, OTP Code: {otp_code}")
            return OtpRes(email=req['email'], otp_code=otp_code, id=inserted_id).__dict__

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error inserting OTP: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def verify(self, email: str, otp_code: int):
        try:
            otp = self.db.otps.find_one({"email": email})
            if otp and otp["otp_code"] == otp_code:
                logger.info(f"Verified OTP for email: {email}")
                return otp
            raise HTTPException(status_code=400, detail="Invalid OTP code")

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error verifying OTP: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def cleanup_expired_otp(self):
        try:
            expired_otps = self.db.otps.find({"expired_at": {"$lte": datetime.utcnow()}})
            for otp in expired_otps:
                self.db.otps.delete_one({"_id": otp["_id"]})

            logger.info("Cleaned up expired OTP records")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error cleaning up expired OTP: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def create_otp(self, otp_data: OTPCreate) -> OTPOut:
        # Logic to create a new OTP in the database
        otp_id = ObjectId()  # Generate a new ObjectId for the OTP
        otp_data_dict = otp_data.dict()
        otp_data_dict["_id"] = otp_id
        self.db.otps.insert_one(otp_data_dict)
        return OTPOut(id=otp_id, **otp_data_dict)

    def get_otps(self, skip: int = 0, limit: int = 10) -> List[OTPOut]:
        # Logic to retrieve a list of OTPs from the database
        otps = list(self.db.otps.find().skip(skip).limit(limit))
        for otp in otps:
            otp["_id"] = str(otp["_id"])
        return otps

    def get_otp(self, otp_id: str) -> Optional[OTPOut]:
        # Logic to retrieve an OTP by its ID from the database
        otp = self.db.otps.find_one({"_id": ObjectId(otp_id)})
        if otp:
            otp["_id"] = str(otp["_id"])
            return otp
        return None

    def update_otp(self, otp_id: str, otp_update: OTPUpdate) -> Optional[OTPOut]:
        # Logic to update an OTP in the database
        update_data = otp_update.dict(exclude_unset=True)
        result = self.db.otps.update_one({"_id": ObjectId(otp_id)}, {"$set": update_data})
        print(result)
        if result:
            updated_otp = self.db.otps.find_one({"_id": ObjectId(otp_id)})
            updated_otp["_id"] = str(updated_otp["_id"])
            return updated_otp
        return None

    def delete_otp(self, otp_id: str) -> Optional[OTPOut]:
        # Logic to delete an OTP from the database
        otp = self.db.otps.find_one({"_id": ObjectId(otp_id)})
        if otp:
            self.db.otps.delete_one({"_id": ObjectId(otp_id)})
            otp["_id"] = str(otp["_id"])
            return otp
        return None


class TokenService:

    def __init__(self):
        self.client = client
        self.db = db

    def insert(self, req: TokenReq):
        req = dict(req)
        try:
            user = UserService().get_by_email(req['email'])
            existing_token = self.db.tokens.find_one({"email": req['email']})

            if existing_token:
                raise HTTPException(
                    status_code=409,
                    detail='A token for this email already exists'
                )

            while True:
                token_value = str(uuid4())
                existing_token = self.db.tokens.find_one({"token": token_value})

                if not existing_token:
                    try:
                        expired_at = datetime.utcnow() + timedelta(hours=1)
                        token_data = {
                            "token": token_value,
                            "email": req['email'],
                            "expired_at": expired_at
                        }
                        self.db.tokens.insert_one(token_data)
                        EmailSender().send_token_email(req['email'], token_data)
                        logger.info(f"Generated and stored token for email: {req['email']}")
                        return token_data
                    except Exception as e:
                        logger.error(f"Failed to generate and store token: {e}")
                        raise HTTPException(
                            status_code=500,
                            detail="Failed to generate and store token"
                        )

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error inserting token: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def verify_token(self, token_value: UUID):
        try:
            token = self.db.tokens.find_one({"token": str(token_value)})
            print(token, 'masd')
            if token and token["expired_at"] >= datetime.utcnow():
                logger.info(f"Verified token for email: {token['email']}")
                return token
            raise HTTPException(status_code=400, detail="Invalid token or token has expired")

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def cleanup_expired_tokens(self):
        try:
            expired_tokens = self.db.tokens.find({"expired_at": {"$lt": datetime.utcnow()}})
            for token in expired_tokens:
                self.db.tokens.delete_one({"_id": token["_id"]})

            logger.info("Cleaned up expired token records")

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error cleaning up expired tokens: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_by_token(self, token_value: UUID):
        try:
            token = self.db.tokens.find_one({"token": str(token_value)})
            if token:
                logger.info(f"Retrieved token for email: {token['email']}")
                return token
            raise HTTPException(status_code=404, detail=f"Token with value '{token_value}' not found")

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error retrieving token by token value: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def create_token(self, token_data: TokenCreate) -> TokenOut:
        token_id = ObjectId()
        token_data_dict = token_data.dict()
        token_data_dict["_id"] = token_id
        self.db.tokens.insert_one(token_data_dict)
        return TokenOut(id=str(token_id), **token_data_dict)

    def get_tokens(self, skip: int = 0, limit: int = 10) -> List[TokenOut]:
        tokens = list(self.db.tokens.find().skip(skip).limit(limit))
        for token in tokens:
            token["_id"] = str(token["_id"])
        return tokens

    def get_token(self, token_id: str) -> Optional[TokenOut]:
        token = self.db.tokens.find_one({"_id": ObjectId(token_id)})
        if token:
            token["_id"] = str(token["_id"])
            return token
        return None

    def update_token(self, token_id: str, token_update: TokenUpdate) -> Optional[TokenOut]:
        update_data = token_update.dict(exclude_unset=True)
        result = self.db.tokens.update_one({"_id": ObjectId(token_id)}, {"$set": update_data})
        if result.modified_count:
            updated_token = self.db.tokens.find_one({"_id": ObjectId(token_id)})
            updated_token["_id"] = str(updated_token["_id"])
            return updated_token
        return None

    def delete_token(self, token_id: str) -> Optional[TokenOut]:
        token = self.db.tokens.find_one({"_id": ObjectId(token_id)})
        if token:
            self.db.tokens.delete_one({"_id": ObjectId(token_id)})
            token["_id"] = str(token["_id"])
            return token
        return None


class PermissionService:

    def __init__(self):
        self.client = client
        self.db = db

    def get_by_name(self, permission_name: str):
        try:
            permission = self.db.permissions.find_one({"name": permission_name})
            if permission:
                logger.info(f"Retrieved permission by name: {permission_name}")
                return permission
            raise HTTPException(status_code=404, detail=f"Permission with name '{permission_name}' not found")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving permission by name: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def create_permission(self, permission_data: PermissionCreate) -> PermissionOut:
        permission_id = ObjectId()
        permission_data_dict = permission_data.dict()
        permission_data_dict["_id"] = permission_id
        self.db.permissions.insert_one(permission_data_dict)
        return PermissionOut(id=str(permission_id), **permission_data_dict)

    def get_permissions(self, skip: int = 0, limit: int = 10) -> List[PermissionOut]:
        permissions = list(self.db.permissions.find().skip(skip).limit(limit))
        for permission in permissions:
            permission["_id"] = str(permission["_id"])
        return permissions

    def get_permission(self, permission_id: str) -> Optional[PermissionOut]:
        permission = self.db.permissions.find_one({"_id": ObjectId(permission_id)})
        if permission:
            permission["_id"] = str(permission["_id"])
            return permission
        return None

    def update_permission(self, permission_id: str, permission_update: PermissionUpdate) -> Optional[PermissionOut]:
        update_data = permission_update.dict(exclude_unset=True)
        result = self.db.permissions.update_one({"_id": ObjectId(permission_id)}, {"$set": update_data})
        if result.modified_count:
            updated_permission = self.db.permissions.find_one({"_id": ObjectId(permission_id)})
            updated_permission["_id"] = str(updated_permission["_id"])
            return updated_permission
        return None

    def delete_permission(self, permission_id: str) -> Optional[PermissionOut]:
        permission = self.db.permissions.find_one({"_id": ObjectId(permission_id)})
        if permission:
            self.db.permissions.delete_one({"_id": ObjectId(permission_id)})
            permission["_id"] = str(permission["_id"])
            return permission
        return None