import os
import uuid
from datetime import datetime, timedelta

from bson import ObjectId
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, Security
from passlib.context import CryptContext
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from jose import jwt, JWTError
from pymongo import MongoClient

from .models import User
from sqlalchemy.orm import Session

from ..db import db
from ..logger import logger
from fastapi_sso.sso.google import GoogleSSO

load_dotenv()

crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users")

sso = GoogleSSO(
    client_id="981508218676-acrnka0o2adpilvqeteg7vhg1hc3mopl.apps.googleusercontent.com",
    client_secret="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",
    redirect_uri="http://localhost:3002/api/auth/callback/google",
    allow_insecure_http=True,
    scope=["profile", "email"]
)

client = MongoClient(os.environ.get("DATABASE_URL"))
# Access your database
db = client["university"]
def get_password_hash(password):
    """
    Hash the password using the CryptContext.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return crypt_context.hash(password)


def create_token(data: dict, expires_delta: timedelta):
    """
    Create an access token with the given data and expiration time.

    Args:
        data (dict): The data to be included in the token.
        expires_delta (timedelta): The duration until the token expires.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    """
    Verify the plain password against the hashed password.

    Args:
        plain_password (str): The plain (unhashed) password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return crypt_context.verify(plain_password, hashed_password)


def authenticate(password, user):
    """
    Authenticate the user with the provided email and password.

    Args:
        password (str): The password entered by the user.
        user: The User object representing the user to authenticate.

    Returns:
        bool: True if authentication is successful, raises HTTPException otherwise.
    """
    try:
        password_check = verify_password(password, user['password'])
        return password_check
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=400, detail="Invalid account")


def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    """
    Get the current user based on the provided token.

    Args:
        security_scopes (SecurityScopes): The security scopes required.
        token (str): The OAuth2 token.

    Returns:
        User: The current authenticated user.

    Raises:
        HTTPException: If credentials cannot be validated or if the user has insufficient permissions.
    """
    print('fffff')
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    print("aaaaa")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        print(user_id)
        if user_id is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
    except JWTError:
        raise credentials_exception
    print("vvvv")
    user = db.users.find_one({"_id": ObjectId(user_id)})
    print(user)
    if user is None:
        raise credentials_exception
    print(user)

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user


def get_user(user: User = Security(get_current_user, scopes=["user"])):
    """
    Get the user based on the current authentication.

    Args:
        user (User): The current authenticated user.

    Returns:
        User: The current authenticated user.
    """
    return user


def get_admin_user(user: User = Security(get_current_user, scopes=["user", "admin"])):
    """
    Get the user based on the current authentication.

    Args:
        user (User): The current authenticated user.

    Returns:
        User: The current authenticated user.
    """
    return user
