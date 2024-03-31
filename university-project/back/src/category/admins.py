from ..core.admins import BaseAdmin
from .models import Category


class CategoryAdmin(BaseAdmin, model=Category):
    """
    Admin class for managing Category objects.

    Attributes:
        category (str): The category label for the admin interface.
        name (str): The singular name for the model in the admin interface.
        name_plural (str): The plural name for the model in the admin interface.
        column_list (list): List of columns to be displayed in the admin interface.
        column_searchable_list (list): List of columns that can be searched in the admin interface.
        column_sortable_list (list): List of columns that can be sorted in the admin interface.
    """
    category = "Category"
    name = "Category"
    name_plural = "Categories"
    column_list = [Category.id, Category.name, Category.parent_id] + BaseAdmin.column_list
    column_searchable_list = [Category.id, Category.name, Category.parent_id]
    column_sortable_list = [Category.name, Category.parent_id] + BaseAdmin.column_sortable_list
