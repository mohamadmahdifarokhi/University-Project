from ..core.admins import BaseAdmin
from .models import Profile


class ProfileAdmin(BaseAdmin, model=Profile):
    """
    Admin class for managing Profile model in the application.

    Attributes:
        model (Profile): The model associated with this admin class.
        category (str): The category label for the admin interface.
        name (str): The singular name for the model in the admin interface.
        name_plural (str): The plural name for the model in the admin interface.
        column_list (list): List of columns to be displayed in the admin interface.
        column_searchable_list (list): List of columns that can be searched in the admin interface.
        column_sortable_list (list): List of columns that can be sorted in the admin interface.
    """

    category = "Profile"
    name = "Profile"
    name_plural = "Profiles"
    column_list = [Profile.id, Profile.photo, Profile.user_id] + BaseAdmin.column_list
    column_searchable_list = [Profile.id, Profile.user_id]
    column_sortable_list = [Profile.user_id] + BaseAdmin.column_sortable_list
