from typing import List, Optional
from datetime import datetime, date

from typing import List, Optional, Annotated

from pydantic import UUID4, BaseModel

from .models import StatusEnum
from ..auth.schemas import ObjectIdPydanticAnnotation
from bson import ObjectId


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
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
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

    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    transaction_id: str
    price: float
    discount_price: float
    status: StatusEnum
    user_id: UUID4
    class Config:
        arbitrary_types_allowed = True


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

class OrderCreateSchema(BaseModel):
    user_id: Optional[str] = None
    battery_id: str
    seller_id: Optional[str] = None
    amount: int
    fee: Optional[int] = None
    created_at: datetime | None  = None


class OrderOutputSchema(BaseModel):
    user_id: Optional[str] = None
    battery_id: str
    seller_id: Optional[str] = None
    amount: int
    fee: Optional[int] = None
    created_at: str | None  = None

class OrderCreate(BaseModel):
    price: float = 0.0
    status: str
    user_id: str

class OrderUpdate(BaseModel):
    price: Optional[float] = None
    status: Optional[str] = None
    volume: Optional[float] = None




class OrderOut(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    price: float | None = None
    status: str | None = None
    volume: float | None = None
    user_id: str | None = None
    class Config:
        arbitrary_types_allowed = True
