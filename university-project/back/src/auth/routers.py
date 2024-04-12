import json
import random
from datetime import timedelta
from uuid import UUID

import requests
from fastapi import APIRouter, Depends, HTTPException, Security, Form, Request
from sqlalchemy.orm import Session

from .schemas import (OtpReq, OtpRes, TokenRes, VerifyOtpReq, UserRes, TokenReq, VerifyTokenReq, TokenPasswordReq,
                      UserUp, PasswordReq, VerifyCodeReq, SendEmailReq, UserReq)
from ..core.utils import redis_instance, EmailSender
from ..db.db import sess_db, db
from .models import User, PermissionSet
from .services import UserService, TokenService, OTPService, PermissionSetService, PermissionService
from .secures import get_current_user, authenticate, ACCESS_TOKEN_EXPIRE_MINUTES, sso, create_token, \
    REFRESH_TOKEN_EXPIRE_DAYS, get_admin_user
from ..logger import logger
from ..profile.models import Profile

router = APIRouter(tags=["Auths"])


# @router.post("/users", response_model=UserRes)
# def create_user(user_data: UserReq, sess: Session = Depends(sess_db)):
#     user = UserService(sess).insert(user_data)
#     return user

# @router.get("/users/{user_id}", response_model=UserRes,
#             dependencies=[Security(get_current_user, scopes=["admin"])])
# def get_user(user_id: UUID, sess: Session = Depends(sess_db)):
#     user = UserService(sess).get_by_id(user_id)
#     return user

# @router.get("/users",
#             dependencies=[Security(get_current_user, scopes=["admin"])])
# def get_users(sess: Session = Depends(sess_db)):
#     """
#     Endpoint to list all users.
#
#     Args:
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         List[User]: List of user objects.
#     """
#     return UserService(sess).get_all()

# @router.patch("/users/{user_id}", response_model=UserRes,
#               dependencies=[Security(get_current_user, scopes=["admin"])])
# def update_user(user_id: UUID, user_data: UserReq, sess: Session = Depends(sess_db)):
#     user = UserService(sess).update(user_id, user_data)
#     return user

# @router.delete("/users/{user_id}", response_model=dict,
#                dependencies=[Security(get_current_user, scopes=["admin"])])
# def delete_user(user_id: UUID, sess: Session = Depends(sess_db)):
#     UserService(sess).delete(user_id)
@router.post("/test", status_code=200)
def test():
    user = UserReq(email='a@gmail.com', password='password')

    result = db["user"].insert_one(user.__dict__)

    return {"message": "User inserted successfully"}


@router.post("/users", status_code=200)
def access_token(
        username: str = Form(...),
        password: str = Form(...),
        authCode: str = Form(None),
        sess: Session = Depends(sess_db)

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

    r_token, user_id, expires_delta_r, r_scopes = UserService(sess).create_token(
        username, password, token_type="refresh", auth=True
    )

    a_token, _, expires_delta_a, a_scopes = UserService(sess).create_token(
        username, password, auth=True
    )

    if authCode:
        token_data = [str(a_token), str(r_token)]
        token_data_json = json.dumps(token_data)
        redis_instance.set(str(authCode), token_data_json, ACCESS_TOKEN_EXPIRE_MINUTES * 60)
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
async def refresh_token(user: User = Security(get_current_user, scopes=["user"]), sess: Session = Depends(sess_db)):
    """
    Endpoint to refresh an access token.

    Args:
        user (User): Currently authenticated user.
        sess (Session): SQLAlchemy database session.

    Returns:
        dict: New access token information.
    """
    a_token, _, _, scopes = UserService(sess).create_token(user.email, user.password)

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
#     # user = UserService(sess).get_by_email(client_id)
#     # scopes = PermissionSetService(sess).get_by_user_id(user.id)
#     # auth_code = f"{user.email}:{user.password}:user"
#     # return RedirectResponse(
#     #     url=f"{redirect_uri}?code={auth_code}&grant_type={response_type}&redirect_uri={redirect_uri}&state={state}"
#     # )


@router.post("/users/otp", response_model=OtpRes)
def send_otp(req: OtpReq, sess: Session = Depends(sess_db)):
    """
    Endpoint to send OTP.

    Args:
        req (OtpReq): OTP request model.
        sess (Session): SQLAlchemy database session.

    Returns:
        OtpRes: OTP response model.
    """
    otp = OTPService(sess).insert(req)
    return otp


# @router.post("/users/otp/verify", response_model=UserRes)
@router.post("/users/otp/verify")
def otp_verify(req: VerifyOtpReq, sess: Session = Depends(sess_db)):
    """
    Endpoint to verify OTP.

    Args:
        req (VerifyOtpReq): Verify OTP request model.
        sess (Session): SQLAlchemy database session.

    Returns:
        UserRes: User response model.
    """
    user = UserService(sess).insert(req)
    print(user, "dede")
    return user


@router.post("/users/recover", response_model=TokenRes)
def recover(req: TokenReq, sess: Session = Depends(sess_db)):
    """
    Endpoint to send token for password recovery.

    Args:
        req (TokenReq): Token request model.
        sess (Session): SQLAlchemy database session.

    Returns:
        TokenRes: Token response model.
    """
    token = TokenService(sess).insert(req)
    return token


@router.post("/users/recover/verify", response_model=TokenRes)
def recover_verify(req: VerifyTokenReq, sess: Session = Depends(sess_db)):
    """
    Endpoint to verify the recovery token.

    Args:
        req (VerifyTokenReq): Verify token request model.
        sess (Session): SQLAlchemy database session.

    Returns:
        bool: True if the token is valid.
    """
    return TokenService(sess).verify_token(req.token)


@router.post("/users/recover/password", response_model=UserRes)
def recover_password(req: TokenPasswordReq, sess: Session = Depends(sess_db)):
    """
    Endpoint to change password using the recovery token.

    Args:
        req (TokenPasswordReq): Change password with token request model.
        sess (Session): SQLAlchemy database session.

    Returns:
        user (UserRes): return user.
    """
    token = TokenService(sess).get_by_token(req.token)
    user = UserService(sess).get_by_email(token.email)

    if not authenticate(req.password, user):
        return UserService(sess).update(user.id, UserUp(password=req.password))
    else:
        raise HTTPException(status_code=400, detail="Current password and new password must be different")


@router.post("/users/password", response_model=UserRes)
def user_password(req: PasswordReq, sess: Session = Depends(sess_db), user: User = Depends(get_current_user)):
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
            user_service = UserService(sess)
            account = user_service.get_by_email(user.email)
            return user_service.update(account.id, UserUp(password=req.new_password))
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
async def auth_callback(request: Request, sess: Session = Depends(sess_db)):
    """Verify login"""
    with sso:
        user = await sso.verify_and_process(request)
        email = user.email

    try:
        # user = UserService(sess).get_by_email(user.email)
        user = sess.query(User).filter_by(email=email).first()
        if not user:
            user = User(email=email)
            sess.add(user)
            permission_service = PermissionService(sess)
            user_permission = permission_service.get_by_name("user")
            user_permission_set = PermissionSet(user=user, permission_id=user_permission.id)
            sess.add(user_permission_set)
            random_numbers = random.randint(1, 26)
            profile = Profile(user=user, photo=random_numbers)
            sess.add(profile)

            cart = Cart(user=user)
            sess.add(cart)

            sess.commit()
            a_token, _, expires_delta_a, a_scopes = UserService(sess).create_token(
                user.email, user.password, auth=False
            )
            headers = {'content-type': "application/json", 'access-token': f'Bearer {a_token}'}
            payload = {
                'userId': str(user.id)
            }
            response = requests.post('http://127.0.0.1:8001/shared-account/', json=payload, headers=headers)
            if response.status_code != 201:
                raise HTTPException(status_code=400, detail="Failed to create shared account for the user.")

            logger.info(f"Inserted User with ID: {user.id}, Email: {email}")
            logger.info(f"Inserted Profile with ID: {profile.id}, User ID: {user.id}")
            logger.info(f"Inserted Cart with ID: {cart.id}, User ID: {user.id}")

        scopes = PermissionSetService(sess).get_by_user_id(user.id)

        a_token = create_token(
            data={"sub": str(user.id), "scopes": [scope.permission.name for scope in scopes]},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        r_token = create_token(
            data={"sub": str(user.id), "scopes": [scope.permission.name for scope in scopes]},
            expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS),
        )
        logger.info(f"Token created for User with ID: {user.id}, Email: {email}")
        return {
            "access_token": a_token,
            "expires_in": timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds(),
            "token_type": "Bearer",
            "user_id": user.id,
            "email": email,
            "refresh_token": r_token
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating token: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# @router.post("/permissions", response_model=PermissionRes,
#              dependencies=[Security(get_current_user, scopes=["admin"])])
# def create_permission(permission_data: PermissionReq, sess: Session = Depends(sess_db)):
#     """
#     Create a new permission.
#
#     Args:
#         permission_data (PermissionReq): Permission request model.
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         PermissionRes: Created permission.
#     """
#     permission_service = PermissionService(sess)
#     permission = Permission(name=permission_data.name, description=permission_data.description)
#
#     if permission_service.insert(permission):
#         return permission
#     else:
#         raise HTTPException(status_code=500, detail="Failed to create permission")


# @router.get("/permissions", response_model=List[PermissionRes],
#             dependencies=[Security(get_current_user, scopes=["admin"])])
# def list_permissions(sess: Session = Depends(sess_db)):
#     """
#     Get a list of all permissions.
#
#     Args:
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         List[PermissionRes]: List of permissions.
#     """
#     permission_service = PermissionService(sess)
#     permissions = permission_service.get_all()
#     return permissions


# @router.get("/permissions/{permission_id}", response_model=PermissionRes,
#             dependencies=[Security(get_current_user, scopes=["admin"])])
# def get_permission(permission_id: UUID, sess: Session = Depends(sess_db)):
#     """
#     Get a permission by ID.
#
#     Args:
#         permission_id (UUID): Permission ID.
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         PermissionRes: Permission details.
#     """
#     permission_service = PermissionService(sess)
#     permission = permission_service.get_by_id(permission_id)
#     return permission


# @router.patch("/permissions/{permission_id}", response_model=PermissionRes,
#               dependencies=[Security(get_current_user, scopes=["admin"])])
# def update_permission(permission_id: UUID, permission_data: PermissionReq, sess: Session = Depends(sess_db)):
#     """
#     Update a permission.
#
#     Args:
#         permission_id (UUID): Permission ID.
#         permission_data (PermissionReq): Permission request model.
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         PermissionRes: Updated permission details.
#     """
#     permission_service = PermissionService(sess)
#
#     if permission_service.update(permission_id, permission_data):
#         return {"message": "Permission updated successfully", "id": permission_id}
#     else:
#         raise HTTPException(status_code=500, detail="Failed to update permission")


# @router.delete("/permissions/{permission_id}", response_model=dict,
#                dependencies=[Security(get_current_user, scopes=["admin"])])
# def delete_permission(permission_id: UUID, sess: Session = Depends(sess_db)):
#     """
#     Delete a permission.
#
#     Args:
#         permission_id (UUID): Permission ID.
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         dict: Success message.
#     """
#     permission_service = PermissionService(sess)
#
#     if permission_service.delete(permission_id):
#         return {"message": "Permission deleted successfully"}
#     else:
#         raise HTTPException(status_code=500, detail="Failed to delete permission")


# @router.post("/permissions-set", response_model=PermissionSetRes,
#              dependencies=[Security(get_current_user, scopes=["admin"])])
# def create_permission_set(permission_set_data: PermissionSetReq, sess: Session = Depends(sess_db)):
#     """
#     Create a new permission set.
#
#     Args:
#         permission_set_data (PermissionSetReq): Permission set request model.
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         PermissionSetRes: Created permission set.
#     """
#     permission_set = PermissionSet(user_id=permission_set_data.user_id,
#                                    permission_id=permission_set_data.permission_id)
#
#     return PermissionSetService(sess).insert(permission_set)


# @router.get("/permissions-set", response_model=List[PermissionSetRes],
#             dependencies=[Security(get_current_user, scopes=["admin"])])
# def list_permission_sets(sess: Session = Depends(sess_db)):
#     """
#     Get a list of all permission sets.
#
#     Args:
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         List[PermissionSetRes]: List of permission sets.
#     """
#     permission_set_service = PermissionSetService(sess)
#     permission_sets = permission_set_service.get_all()
#     return permission_sets


# @router.get("/permissions-set/{permission_set_id}", response_model=PermissionSetRes,
#             dependencies=[Security(get_current_user, scopes=["admin"])])
# def get_permission_set(permission_set_id: UUID, sess: Session = Depends(sess_db)):
#     """
#     Get a permission set by ID.
#
#     Args:
#         permission_set_id (UUID): Permission set ID.
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         PermissionSetRes: Permission set details.
#     """
#     permission_set_service = PermissionSetService(sess)
#     permission_set = permission_set_service.get_by_id(permission_set_id)
#     return permission_set


# @router.patch("/permissions-set/{permission_set_id}", response_model=PermissionSetRes,
#               dependencies=[Security(get_current_user, scopes=["admin"])])
# def update_permission_set(permission_set_id: UUID, permission_set_data: PermissionSetUp,
#                           sess: Session = Depends(sess_db)):
#     """
#     Update a permission set.
#
#     Args:
#         permission_set_id (UUID): Permission set ID.
#         permission_set_data (PermissionSetReq): Permission set request model.
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         PermissionSetRes: Updated permission set details.
#     """
#     return PermissionSetService(sess).update(permission_set_id, permission_set_data)


# @router.delete("/permissions-set/{permission_set_id}",
#                dependencies=[Security(get_current_user, scopes=["admin"])])
# def delete_permission_set(permission_set_id: UUID, sess: Session = Depends(sess_db)):
#     """
#     Delete a permission set.
#
#     Args:
#         permission_set_id (UUID): Permission set ID.
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         dict: Success message.
#     """
#     return PermissionSetService(sess).delete(permission_set_id)
