from ..core.admins import BaseAdmin
from .models import Order, OrderItem


class OrderAdmin(BaseAdmin, model=Order):
    """
    Admin class for managing Order models in the admin interface.

    Attributes:
    - category (str): Category name for the admin interface.
    - name (str): Singular name of the model.
    - name_plural (str): Plural name of the model.
    - column_list (List): List of columns to be displayed in the admin list view.
    - column_searchable_list (List): List of columns that can be searched in the admin interface.
    - column_sortable_list (List): List of columns that can be used for sorting in the admin interface.
    """

    category = "Order"
    name = "Order"
    name_plural = "Orders"
    column_list = [
        Order.id,
        Order.transaction_id,
        Order.price,
        Order.discount_price,
        Order.status,
        Order.user_id,
    ] + BaseAdmin.column_list
    column_searchable_list = [Order.id, Order.transaction_id, Order.user_id]
    column_sortable_list = (
        [Order.transaction_id, Order.price, Order.discount_price, Order.status, Order.user_id]
        + BaseAdmin.column_sortable_list
    )


class OrderItemAdmin(BaseAdmin, model=OrderItem):
    """
    Admin class for managing OrderItem models in the admin interface.

    Attributes:
    - category (str): Category name for the admin interface.
    - name (str): Singular name of the model.
    - name_plural (str): Plural name of the model.
    - column_list (List): List of columns to be displayed in the admin list view.
    - column_searchable_list (List): List of columns that can be searched in the admin interface.
    - column_sortable_list (List): List of columns that can be used for sorting in the admin interface.
    """

    category = "Order"
    name = "OrderItem"
    name_plural = "order_items"
    column_list = [
        OrderItem.id,
        OrderItem.name,
        OrderItem.price,
        OrderItem.discount_price,
        OrderItem.email,
        OrderItem.password,
        OrderItem.description,
        OrderItem.status,
        OrderItem.orderId,
        OrderItem.product_id,
    ] + BaseAdmin.column_list
    column_searchable_list = [
        OrderItem.id,
        OrderItem.name,
        OrderItem.email,
        OrderItem.orderId,
        OrderItem.product_id,
    ]
    column_sortable_list = (
        [OrderItem.name, OrderItem.price, OrderItem.discount_price, OrderItem.status, OrderItem.orderId,
         OrderItem.product_id]
        + BaseAdmin.column_sortable_list
    )
