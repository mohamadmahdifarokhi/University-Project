import json
import random
import uuid
from datetime import timedelta
from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException, Security, Form, Request
from sqlalchemy.orm import Session

from .schemas import (OtpReq, OtpRes, TokenRes, VerifyOtpReq, UserRes, TokenReq, VerifyTokenReq, TokenPasswordReq,
                      UserUp, PasswordReq, VerifyCodeReq, SendEmailReq, UserReq, UserUpdate, UserOut, UserCreate)
from ..core.utils import redis_instance, EmailSender
from ..db.db import sess_db, db
from .models import User
from .services import UserService, TokenService, OTPService, PermissionService
from .secures import get_current_user, authenticate, ACCESS_TOKEN_EXPIRE_MINUTES, sso, create_token, \
    REFRESH_TOKEN_EXPIRE_DAYS, get_admin_user
from ..logger import logger
from ..profile.models import Profile

router = APIRouter(tags=["Auths"])



@router.post("/users", status_code=200)
def access_token(
        username: str = Form(...),
        password: str = Form(...),
        authCode: str = Form(None),
):
    """
    Endpoint to generate an access token.

    Args:
        authCode:
        username (str): User's username.
        password (str): User's password.
        sess (Session): SQLAlchemy database session.

    Returns:
        dict: Access token information.
    """

    r_token, user_id, expires_delta_r, r_scopes = UserService().create_token(
        username, password, token_type="refresh", auth=True
    )

    a_token, _, expires_delta_a, a_scopes = UserService().create_token(
        username, password, auth=True
    )

    return {
        "access_token": a_token,
        "expires_in": expires_delta_a.total_seconds(),
        "token_type": "Bearer",
        "user_id": user_id,
        "email": username,
        "refresh_token": r_token,
        "scopes": a_scopes

    }


@router.post("/users/refresh", status_code=200)
async def refresh_token(user: User = Security(get_current_user, scopes=["user"])):
    """
    Endpoint to refresh an access token.

    Args:
        user (User): Currently authenticated user.
        sess (Session): SQLAlchemy database session.

    Returns:
        dict: New access token information.
    """
    a_token, _, _, scopes = UserService().create_token(user['email'], user['password'])

    return {"access_token": a_token, "scopes": scopes, "token_type": "Bearer"}


@router.post("/admins/email", status_code=200, dependencies=[Security(get_admin_user)])
async def send_email(req: SendEmailReq):
    """
    Endpoint to refresh an access token.

    Args:
        req:
    """
    EmailSender().send_email(req.subject, req.email, req.description)
    return True


@router.post("/users/code/verify")
def code_verify(req: VerifyCodeReq):
    """
    Endpoint to verify code.

    Args:
        req (VerifyCodeReq): Verify code request model.

    Returns:
        dict: Access token information.
    """
    token_data_json = redis_instance.get(req.code)
    if token_data_json:
        token_data = json.loads(token_data_json)
        a_token = token_data[0]
        r_token = token_data[1]
        redis_instance.delete(req.code)
        return {
            "access_token": a_token,
            "token_type": "Bearer",
            "refresh_token": r_token
        }
    raise HTTPException(status_code=400, detail="Invalid Auth Code")


# @router.get("/oauth2/authorize")
# def authorization_url(form_data: OAuth2PasswordRequestForm = Depends(),
#                       sess: Session = Depends(sess_db)):
#     """
#     Endpoint to generate authorization URL.
#
#     Args:
#         state (str): State parameter for additional security.
#         client_id (str): Client ID for the OAuth2 client.
#         redirect_uri (str): Redirect URI for callback.
#         response_type (str): Response type (e.g., "code").
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         RedirectResponse: Redirects to the provided URI with authorization code.
#     """
#     print(form_data)
#     # user = UserService().get_by_email(client_id)
#     # scopes = PermissionSetService().get_by_user_id(user.id)
#     # auth_code = f"{user.email}:{user.password}:user"
#     # return RedirectResponse(
#     #     url=f"{redirect_uri}?code={auth_code}&grant_type={response_type}&redirect_uri={redirect_uri}&state={state}"
#     # )


# @router.post("/users/otp")
@router.post("/users/otp", response_model=OtpRes)
def send_otp(req: OtpReq):
    """
    Endpoint to send OTP.

    Args:
        req (OtpReq): OTP request model.
        sess (Session): SQLAlchemy database session.

    Returns:
        OtpRes: OTP response model.
    """
    otp = OTPService().insert(req)
    return otp


# @router.post("/users/otp/verify", response_model=UserRes)
@router.post("/users/otp/verify")
def otp_verify(req: VerifyOtpReq):
    """
    Endpoint to verify OTP.

    Args:
        req (VerifyOtpReq): Verify OTP request model.
        sess (Session): SQLAlchemy database session.

    Returns:
        UserRes: User response model.
    """
    user = UserService().insert(req)
    print(user, "dede")
    return user


@router.post("/users/recover", response_model=TokenRes)
def recover(req: TokenReq):
    """
    Endpoint to send token for password recovery.

    Args:
        req (TokenReq): Token request model.
        sess (Session): SQLAlchemy database session.

    Returns:
        TokenRes: Token response model.
    """
    token = TokenService().insert(req)
    return token


@router.post("/users/recover/verify", response_model=TokenRes)
def recover_verify(req: VerifyTokenReq):
    """
    Endpoint to verify the recovery token.

    Args:
        req (VerifyTokenReq): Verify token request model.
        sess (Session): SQLAlchemy database session.

    Returns:
        bool: True if the token is valid.
    """
    return TokenService().verify_token(req.token)


@router.post("/users/recover/password", response_model=UserRes)
def recover_password(req: TokenPasswordReq):
    req = dict(req)
    """
    Endpoint to change password using the recovery token.

    Args:
        req (TokenPasswordReq): Change password with token request model.
        sess (Session): SQLAlchemy database session.

    Returns:
        user (UserRes): return user.
    """
    print('asdasd')
    token = TokenService().get_by_token(req['token'])
    print('asdsssssasd')

    user = UserService().get_by_email(token['email'])
    print('asdcasd')

    if not authenticate(req['password'], user):
        return UserService().update(user['_id'], UserUp(password=req['password']))
    else:
        raise HTTPException(status_code=400, detail="Current password and new password must be different")


@router.post("/users/password", response_model=UserRes)
def user_password(req: PasswordReq, user: User = Depends(get_current_user)):
    """
    Endpoint to change user password.

    Args:
        req (PasswordReq): Change password request model.
        sess (Session): SQLAlchemy database session.
        user (User): Currently authenticated user.

    Returns:
        user (UserRes): return user.
    """
    if authenticate(req.password, user):
        if req.password != req.new_password:
            user_service = UserService()
            account = user_service.get_by_email(user['email'])
            return user_service.update(account['_id'], UserUp(password=req.new_password))
        else:
            raise HTTPException(status_code=400, detail="Current password and new password must be different")
    else:
        raise HTTPException(status_code=400, detail="Invalid password")


@router.get("/auth/login")
async def auth_init(redirect_uri):
    """Initialize auth and redirect"""
    with sso:
        redirect_response = await sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"},
                                                         state=redirect_uri)
        return redirect_response.headers.get("location")


@router.get("/auth/callback")
async def auth_callback(request: Request):
    """Verify login"""
    try:
        # Assuming you have a function to get the MongoDB client
        with sso:
            user = await sso.verify_and_process(request)
            email = user.email

        user = db.users.find_one({"email": email})
        if not user:
            user = {"email": email}
            user_id = db.users.insert_one(user).inserted_id
            permission_service = PermissionService()
            user_permission = permission_service.get_by_name("user")
            permission_set = {"user_id": user_id, "permission_id": user_permission.id}
            db.permission_set.insert_one(permission_set)
            random_numbers = random.randint(1, 26)
            profile = {"user_id": user_id, "photo": random_numbers}
            db.profile.insert_one(profile)
            cart = {"user_id": user_id}
            db.cart.insert_one(cart)

            a_token = create_token(
                data={"sub": str(user_id), "scopes": ["user"]},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            )
            r_token = create_token(
                data={"sub": str(user_id), "scopes": ["user"]},
                expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            )
            logger.info(f"Inserted User with ID: {user_id}, Email: {email}")
            logger.info("Inserted Profile, Cart")
            return {
                "access_token": a_token,
                "expires_in": timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds(),
                "token_type": "Bearer",
                "user_id": str(user_id),
                "email": email,
                "refresh_token": r_token
            }
        else:
            a_token = create_token(
                data={"sub": str(user["_id"]), "scopes": [scope.permission.name for scope in scopes]},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            )
            r_token = create_token(
                data={"sub": str(user["_id"]), "scopes": [scope.permission.name for scope in scopes]},
                expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            )
            logger.info(f"Token created for User with ID: {user['_id']}, Email: {email}")
            return {
                "access_token": a_token,
                "expires_in": timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds(),
                "token_type": "Bearer",
                "user_id": str(user["_id"]),
                "email": email,
                "refresh_token": r_token
            }
    except Exception as e:
        logger.error(f"Error creating token: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/users/create", response_model=UserOut)
async def create_user(user: UserCreate):
    """
    Create a new user.
    """
    return UserService().create_user(user)


@router.get("/users/reads")
async def read_users(skip: int = 0, limit: int = 10):
    """
    Get a list of users.
    """
    return UserService().get_users(skip=skip, limit=limit)


@router.get("/users/read/{user_id}")
async def read_user(user_id):
    """
    Get a user by ID.
    """
    user = UserService().get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/update/{user_id}")
async def update_user(user_id, user_update: UserUpdate):
    """
    Update a user.
    """
    updated_user = UserService().update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/users/delete/{user_id}")
async def delete_user(user_id):
    """
    Delete a user.
    """
    deleted_user = UserService().delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user