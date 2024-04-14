from typing import List

from pydantic import UUID4, BaseModel

from .models import StatusEnum



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


class OrderResList(BaseModel):
    """
    Response model for retrieving a list of orders.

    Attributes:
    - orders (List[OrderRes]): List of order information.
    - count (int): Total count of orders.
    """

    orders: List[OrderRes] | None = None
    count: int

