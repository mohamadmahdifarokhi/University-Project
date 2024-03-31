from typing import List
from pydantic import UUID4, BaseModel, EmailStr

from src.auth.schemas import UserRes
from src.product.schemas import ProductRes


class CartItemReq(BaseModel):
    """
    Request model for creating a CartItem.

    Attributes:
        product_id (UUID4): UUID4 representing the associated product.
        email (EmailStr): Email associated with the item (optional).
        password (str): Password associated with the item (optional).
        description (str): Description of the item (optional).
    """
    product_id: UUID4
    email: EmailStr | None = None
    password: str | None = None
    description: str | None = None


class CartItemRes(BaseModel):
    """
    Response model for a CartItem.

    Attributes:
        product (ProductRes): ProductRes model representing the associated product.
        email (EmailStr): Email associated with the item (optional).
        password (str): Password associated with the item (optional).
        description (str): Description of the item (optional).
    """
    id: UUID4
    product: ProductRes
    email: EmailStr | None = None
    password: str | None = None
    description: str | None = None


# class CartItemUp(BaseModel):
#     """
#     Update model for partially updating a CartItem.
#
#     Attributes:
#         email (EmailStr): Updated email associated with the item (optional).
#         password (str): Updated password associated with the item (optional).
#         description (str): Updated description of the item (optional).
#     """
#     email: EmailStr | None = None
#     password: str | None = None
#     description: str | None = None


# class CartReq(BaseModel):
#     """
#     Request model for creating a Cart.
#     """
#     user_id: UUID4


class CartRes(BaseModel):
    """
    Response model for a Cart.

    Attributes:
        user (UserRes): UserRes model representing the associated user.
        cart_items (List[CartItemRes]): List of CartItemRes models representing items in the cart.
    """
    user: UserRes
    cart_items: List[CartItemRes]

# class CartUpdate(BaseModel):
#     """
#     Update model for partially updating a Cart.
#     """
#     user_id: UUID4 | None = None
