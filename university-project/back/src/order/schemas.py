from typing import List

from pydantic import UUID4, BaseModel

from .models import StatusEnum
from ..product.schemas import ProductRes


class OrderItemReq(BaseModel):
    """
    Request model for creating an order item.

    Attributes:
    - name (dict): Name of the order item.
    - price (float): Regular price of the order item.
    - discount_price (float): Discounted price of the order item.
    - email (str | None): Email associated with the order item (optional).
    - password (str | None): Password associated with the order item (optional).
    - description (str | None): Description of the order item (optional).
    - status (str): Status of the order item.
    - orderId (UUID4): Unique identifier of the associated order.
    - product_id (UUID4): Unique identifier of the associated product.
    """
    name: dict
    price: float
    discount_price: float
    email: str | None = None
    password: str | None = None
    description: str | None = None
    status: str
    orderId: UUID4
    product_id: UUID4


class OrderItemRes(BaseModel):
    """
    Response model for retrieving order item information.

    Attributes:
    - id (UUID4): Unique identifier for the order item.
    - name (dict): Name of the order item.
    - price (float): Regular price of the order item.
    - discount_price (float): Discounted price of the order item.
    - email (str): Email associated with the order item.
    - password (str): Password associated with the order item.
    - description (str): Description of the order item.
    - count (int): Quantity of the order item.
    - status (StatusEnum): Status of the order item.
    - orderId (UUID4): Unique identifier of the associated order.
    - product (ProductRes): Product information associated with the order item.
    """

    id: UUID4
    name: dict
    price: float
    discount_price: float
    email: str | None = None
    password: str | None = None
    description: str | None = None
    status: StatusEnum
    orderId: UUID4
    product: ProductRes


# class OrderItemUp(BaseModel):
#     name: str = None
#     price: float = None
#     discount_price: float = None
#     email: str = None
#     password: str = None
#     description: str = None
#     count: int = None
#     status: str = None
#     orderId: UUID4 = None
#     product_id: UUID4 = None


class OrderReq(BaseModel):
    """
    Request model for creating an order.

    Attributes:
    - user_id (UUID4): Unique identifier of the user who placed the order.
    - transaction_id (str): Transaction ID associated with the order.
    - price (float): Regular price of the order.
    - discount_price (float): Discounted price of the order.
    - status (str): Status of the order.
    """
    user_id: UUID4
    transaction_id: str
    price: float
    discount_price: float
    status: str


class OrderRes(BaseModel):
    """
    Response model for retrieving order information.

    Attributes:
    - id (UUID4): Unique identifier for the order.
    - user_id (UUID4): Unique identifier of the user who placed the order.
    - transaction_id (str): Transaction ID associated with the order.
    - price (float): Regular price of the order.
    - discount_price (float): Discounted price of the order.
    - status (StatusEnum): Status of the order.
    - orderItem (List[OrderItemRes]): List of order items associated with the order.
    """

    id: UUID4
    transaction_id: str
    price: float
    discount_price: float
    status: StatusEnum
    user_id: UUID4
    order_items: List[OrderItemRes] | None = None


class OrderResList(BaseModel):
    """
    Response model for retrieving a list of orders.

    Attributes:
    - orders (List[OrderRes]): List of order information.
    - count (int): Total count of orders.
    """

    orders: List[OrderRes] | None = None
    count: int

# class OrderUp(BaseModel):
#     user_id: UUID4 = None
#     coupon_id: UUID4 = None
#     transaction_id: str = None
#     price: float = None
#     discount_price: float = None
#     status: StatusEnum = None
