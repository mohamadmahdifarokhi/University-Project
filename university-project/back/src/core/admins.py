import os
from typing import Union

import pytz
from dotenv import load_dotenv
from fastapi.security import SecurityScopes
from sqladmin import ModelView, action
from fastapi.responses import RedirectResponse
from datetime import datetime

from starlette.requests import Request

from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.orm import Session
from starlette.responses import Response

from src.auth.secures import get_current_user
from src.auth.services import UserService
from src.db.db import sess_db
from src.logger import logger

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


class BaseAdmin(ModelView):
    """
    Base class for administering models with common actions like deactivation, deletion, activation, and restoration.

    Attributes:
        can_export (bool): Indicates whether the model data can be exported.
        column_sortable_list (list): Columns that can be sorted.
        column_list (list): Columns to be displayed.

    Methods:
        date_format(value): Formats the datetime value to a specific string format.
        _perform_action(request, pks, update_data): Performs a common action on selected items.
        deactivate(request): Deactivates selected items.
        delete(request): Deletes selected items.
        activate(request): Activates selected items.
        restore(request): Restores selected items.
    """

    can_export = True
    column_sortable_list = ["is_active", "is_deleted", "created", "last_updated"]
    column_list = ["is_active", "is_deleted", "created", "last_updated"]

    @staticmethod
    def date_format(value):
        """
        Formats the given datetime value to a specific string format.

        Args:
            value: The datetime value to be formatted.

        Returns:
            str: The formatted datetime string.
        """
        return value.strftime("%Y-%M-%D %H:%M:%S")

    column_type_formatters = {"datetime": date_format}

    async def _perform_action(self, request: Request, pks: list, update_data: dict):
        """
        Performs a common action on selected items.

        Args:
            request (Request): The incoming request.
            pks (list): List of primary keys of selected items.
            update_data (dict): Data to be updated in the selected items.
        """
        print(pks, "lqwdqwd")
        if pks:
            for pk in pks:
                await self.get_object_for_edit(pk)
                await self.update_model(request, pk, update_data)
            referer = request.headers.get("Referer")
            print(referer, "wefwef")
            if referer:
                return RedirectResponse(referer)
            else:
                return RedirectResponse(request.url_for("admin:list", identity=self.identity))

    @action(
        name="Deactivate",
        label="Deactivate",
        confirmation_message="Are you sure you want to deactivate the selected items?",
        add_in_detail=True,
        add_in_list=True
    )
    async def deactivate(self, request: Request):
        """
        Deactivates selected items.

        Args:
            request (Request): The incoming request.
        """
        pks = request.query_params.get("pks", "").split(",")
        return await self._perform_action(request, pks, {"is_active": False})

    @action(
        name="Delete",
        label="Delete",
        confirmation_message="Are you sure you want to delete the selected items?",
        add_in_detail=True,
        add_in_list=True
    )
    async def delete(self, request: Request):
        """
        Deletes selected items.

        Args:
            request (Request): The incoming request.
        """
        pks = request.query_params.get("pks", "").split(",")
        deleted_at = datetime.now(pytz.utc).isoformat()
        return await self._perform_action(request, pks, {"is_active": False, "is_deleted": True, "deleted_at": deleted_at})

    @action(
        name="Activate",
        label="Activate",
        confirmation_message="Are you sure you want to activate the selected items?",
        add_in_detail=True,
        add_in_list=True
    )
    async def activate(self, request: Request):
        """
        Activates selected items.

        Args:
            request (Request): The incoming request.
        """
        pks = request.query_params.get("pks", "").split(",")
        return await self._perform_action(request, pks, {"is_active": True})

    @action(
        name="Restore",
        label="Restore",
        confirmation_message="Are you sure you want to restore the selected items?",
        add_in_detail=True,
        add_in_list=True
    )
    async def restore(self, request: Request):
        """
        Restores selected items.

        Args:
            request (Request): The incoming request.
        """
        pks = request.query_params.get("pks", "").split(",")
        restored_at = datetime.now(pytz.utc).isoformat()
        return await self._perform_action(
            request, pks, {"is_active": True, "is_deleted": False, "restored_at": restored_at}
        )


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        """
        Initializes the AdminAuth instance.

        Args:
            secret_key (str): Secret key for authentication.
        """
        super().__init__(secret_key)

    async def login(self, request: Request, sess: Session = next(sess_db())) -> bool:
        """
        Logs in the administrator.

        Args:
            request (Request): The incoming request.
            sess (Session): SQLAlchemy database session.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        try:
            form = await request.form()
            email = form.get("username")
            password = form.get("password")

            if not email or not password:
                return False

            r_token, _, _, _ = UserService(sess).create_token(email, password, token_type="refresh", auth=True)
            a_token, _, _, _ = UserService(sess).create_token(email, password, auth=True)

            request.session["access_token"] = str(a_token)
            request.session["refresh_token"] = str(r_token)
            return True

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False

    async def logout(self, request: Request) -> bool:
        """
        Logs out the administrator.

        Args:
            request (Request): The incoming request.

        Returns:
            bool: True if logout is successful, False otherwise.
        """
        try:
            request.session.clear()
            return True
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return False

    async def authenticate(self, request: Request, sess: Session = next(sess_db())) -> Union[Response, bool]:
        """
        Authenticates the administrator.

        Args:
            request (Request): The incoming request.
            sess (Session): SQLAlchemy database session.

        Returns:
            Union[Response, bool]: Response if there's an issue, True if authentication is successful, False otherwise.
        """
        try:
            access_token = request.session.get("access_token")
            refresh_token = request.session.get("refresh_token")
            if access_token and refresh_token:
                user = get_current_user(SecurityScopes(["admin"]), refresh_token, sess)
                a_token, _, _, _ = UserService(sess).create_token(user.email, user.password)
                request.session["access_token"] = str(a_token)
                return True
            else:
                return RedirectResponse("/admin/login")

        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False


authentication_backend = AdminAuth(secret_key=SECRET_KEY)
