from typing import Any

from ..core.admins import BaseAdmin
from .models import Product
from .utils import generate_slug


class ProductAdmin(BaseAdmin, model=Product):
    """
    Admin class for managing Product entities.

    Attributes:
    - model (Product): The model associated with this admin class.
    - category (str): The category name for the admin interface.
    - name (str): The singular name for the admin interface.
    - name_plural (str): The plural name for the admin interface.
    - column_list (list): List of columns to be displayed in the admin interface.
    - column_searchable_list (list): List of columns to be searchable in the admin interface.
    - column_sortable_list (list): List of columns to be sortable in the admin interface.
    """

    model = Product
    category = "Product"
    name = "Product"
    name_plural = "Products"
    form_excluded_columns = [Product.slug]
    column_list = [
                      Product.id, Product.name, Product.slug, Product.photo, Product.background, Product.logo, Product.price,
                      Product.discount_price, Product.count, Product.sold
                  ] + BaseAdmin.column_list
    column_searchable_list = [Product.id, Product.name, Product.slug,]
    column_sortable_list = [
                               Product.name, Product.price, Product.discount_price,
                               Product.count, Product.sold
                           ] + BaseAdmin.column_sortable_list

    async def on_model_change(self, data: dict, model: Any, is_created: bool) -> None:
        """
        Event handler called when a model is changed (created or updated).

        Parameters:
        - data (dict): Data representing the changes.
        - model (Any): The model instance being changed.
        - is_created (bool): True if the model is being created, False if updated.
        """
        if "name" in data:
            data["slug"] = data["name"]["en"]
