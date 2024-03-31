from ..core.admins import BaseAdmin
from .models import Cart, CartItem


class CartAdmin(BaseAdmin, model=Cart):
    """
    Admin class for managing Cart objects.

    Attributes:
        category (str): The category label for the admin interface.
        name (str): The singular name for the model in the admin interface.
        name_plural (str): The plural name for the model in the admin interface.
        column_list (list): List of columns to be displayed in the admin interface.
        column_searchable_list (list): List of columns that can be searched in the admin interface.
        column_sortable_list (list): List of columns that can be sorted in the admin interface.
    """
    category = "Cart"
    name = "Cart"
    name_plural = "Carts"
    column_list = [Cart.id, Cart.user_id] + BaseAdmin.column_list
    column_searchable_list = [Cart.id, Cart.user_id]
    column_sortable_list = [Cart.user_id] + BaseAdmin.column_sortable_list


class CartItemAdmin(BaseAdmin, model=CartItem):
    """
    Admin class for managing CartItem objects.

    Attributes:
        category (str): The category label for the admin interface.
        name (str): The singular name for the model in the admin interface.
        name_plural (str): The plural name for the model in the admin interface.
        column_list (list): List of columns to be displayed in the admin interface.
        column_searchable_list (list): List of columns that can be searched in the admin interface.
        column_sortable_list (list): List of columns that can be sorted in the admin interface.
    """
    category = "Cart"
    name = "Cart Item"
    name_plural = "Cart Items"
    column_list = [
                      CartItem.id, CartItem.email, CartItem.password, CartItem.description,
                      CartItem.cart_id, CartItem.product_id
                  ] + BaseAdmin.column_list
    column_searchable_list = [CartItem.id, CartItem.email, CartItem.cart_id, CartItem.product_id]
    column_sortable_list = [
                               CartItem.email, CartItem.description,
                               CartItem.cart_id, CartItem.product_id
                           ] + BaseAdmin.column_sortable_list
