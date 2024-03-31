from .models import OTP, Token, User, Permission, PermissionSet
from ..core.admins import BaseAdmin


class UserAdmin(BaseAdmin, model=User):
    """
    Admin interface for managing User records.

    Attributes:
        category (str): The category under which User records are grouped in the admin interface.
        name (str): The singular name of the admin interface for User records.
        name_plural (str): The plural name of the admin interface for User records.
        column_list (list): List of columns displayed in the admin interface for User records.
        column_searchable_list (list): List of columns that can be searched in the admin interface for User records.
        column_sortable_list (list): List of columns that can be sorted in the admin interface for User records.
    """
    category = "Authentication"
    name = "User"
    name_plural = "Users"
    column_list = [User.id, User.email, User.password] + BaseAdmin.column_list
    column_searchable_list = [User.id, User.email]
    column_sortable_list = [User.email] + BaseAdmin.column_sortable_list


class OTPAdmin(BaseAdmin, model=OTP):
    """
    Admin interface for managing OTP (One-Time Password) records.

    Attributes:
        category (str): The category under which OTP records are grouped in the admin interface.
        name (str): The singular name of the admin interface for OTP records.
        name_plural (str): The plural name of the admin interface for OTP records.
        column_list (list): List of columns displayed in the admin interface for OTP records.
        column_searchable_list (list): List of columns that can be searched in the admin interface for OTP records.
        column_sortable_list (list): List of columns that can be sorted in the admin interface for OTP records.
    """
    category = "Authentication"
    name = "OTP"
    name_plural = "OTPs"
    column_list = [OTP.id, OTP.otp_code, OTP.email, OTP.created, OTP.expired_at] + BaseAdmin.column_list
    column_searchable_list = [OTP.id, OTP.email]
    column_sortable_list = [OTP.email, OTP.created, OTP.expired_at] + BaseAdmin.column_sortable_list


class TokenAdmin(BaseAdmin, model=Token):
    """
    Admin interface for managing Token records.

    Attributes:
        category (str): The category under which Token records are grouped in the admin interface.
        name (str): The singular name of the admin interface for Token records.
        name_plural (str): The plural name of the admin interface for Token records.
        column_list (list): List of columns displayed in the admin interface for Token records.
        column_searchable_list (list): List of columns that can be searched in the admin interface for Token records.
        column_sortable_list (list): List of columns that can be sorted in the admin interface for Token records.
    """
    category = "Authentication"
    name = "Token"
    name_plural = "Tokens"
    column_list = [Token.id, Token.token, Token.email, Token.created, Token.expired_at] + BaseAdmin.column_list
    column_searchable_list = [Token.id, Token.email]
    column_sortable_list = [Token.email, Token.created, Token.expired_at] + BaseAdmin.column_sortable_list


class PermissionAdmin(BaseAdmin, model=Permission):
    """
    Admin interface for managing Permission records.

    Attributes:
        category (str): The category under which Permission records are grouped in the admin interface.
        name (str): The singular name of the admin interface for Permission records.
        name_plural (str): The plural name of the admin interface for Permission records.
        column_list (list): List of columns displayed in the admin interface for Permission records.
        column_searchable_list (list): List of columns that can be searched in the admin interface for Permission records.
        column_sortable_list (list): List of columns that can be sorted in the admin interface for Permission records.
    """
    category = "Authentication"
    name = "Permission"
    name_plural = "Permissions"
    column_list = [Permission.id, Permission.name, Permission.description] + BaseAdmin.column_list
    column_searchable_list = [Permission.id, Permission.name]
    column_sortable_list = [Permission.name] + BaseAdmin.column_sortable_list


class PermissionSetAdmin(BaseAdmin, model=PermissionSet):
    """
    Admin interface for managing PermissionSet records.

    Attributes:
        category (str): The category under which PermissionSet records are grouped in the admin interface.
        name (str): The singular name of the admin interface for PermissionSet records.
        name_plural (str): The plural name of the admin interface for PermissionSet records.
        column_list (list): List of columns displayed in the admin interface for PermissionSet records.
        column_searchable_list (list): List of columns that can be searched in the admin interface for PermissionSet records.
        column_sortable_list (list): List of columns that can be sorted in the admin interface for PermissionSet records.
    """
    category = "Authentication"
    name = "Permission Set"
    name_plural = "Permission Set"
    column_list = [PermissionSet.id, PermissionSet.user_id, PermissionSet.permission_id] + BaseAdmin.column_list
    column_searchable_list = [PermissionSet.id, PermissionSet.user_id, PermissionSet.permission_id]
    column_sortable_list = [PermissionSet.user_id, PermissionSet.permission_id] + BaseAdmin.column_sortable_list
