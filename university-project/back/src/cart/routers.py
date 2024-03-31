from uuid import UUID

from fastapi import APIRouter, Depends, status, Security
from sqlalchemy.orm import Session

from ..auth.models import User
from ..auth.secures import get_user
from .schemas import CartItemRes, CartRes, CartItemReq
from .services import CartService, CartItemService
from ..db.db import sess_db

router = APIRouter(tags=["Carts"])


# @router.post("/",
#              status_code=status.HTTP_201_CREATED,
#              response_model=CartRes,
#              dependencies=[Security(get_current_user, scopes=["admin"])]
#              )
# def create_cart_route(cart: CartReq,
#                       sess: Session = Depends(sess_db)):
#     """Create a new cart."""
#     return CartService(sess).insert(cart)


# @router.get("/{cart_id}",
#             status_code=status.HTTP_200_OK,
#             response_model=CartRes,
#             dependencies=[Security(get_current_user, scopes=["admin"])]
#             )
# def get_cart_by_id_route(cart_id: UUID, sess: Session = Depends(sess_db)):
#     """Retrieve a cart by its ID."""
#     return CartService(sess).get_by_id(cart_id)


@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=CartRes,
            )
def get_cart_by_user_id_route(user: User = Depends(get_user), sess: Session = Depends(sess_db)):
    """
    Retrieve cart with associated cart items and product details by user_id.

    Args:
        user (User): The authenticated user.
        sess (Session): SQLAlchemy database session.

    Returns:
        CartRes: Response model for a cart.
    """
    cart = CartService(sess).get_by_user_id(user)
    return cart


# @router.get("/all",
#             status_code=status.HTTP_200_OK,
#             response_model=List[CartRes],
#             dependencies=[Security(get_current_user, scopes=["admin"])]
#             )
# def get_all_carts_route(sess: Session = Depends(sess_db)):
#     """Retrieve all carts."""
#     carts = CartService(sess).get_all()
#     return carts


# @router.patch("/{cart_id}",
#               status_code=status.HTTP_200_OK,
#               response_model=CartRes,
#               dependencies=[Security(get_current_user, scopes=["admin"])]
#               )
# def update_cart_route(cart_id: UUID, cart: CartUpdate, sess: Session = Depends(sess_db)):
#     """Partially update a cart."""
#     return CartService(sess).update(cart_id, cart)


# @router.delete("/{cart_id}",
#                status_code=status.HTTP_204_NO_CONTENT,
#                dependencies=[Security(get_current_user, scopes=["admin"])]
#                )
# def delete_cart_route(cart_id: UUID, sess: Session = Depends(sess_db)):
#     """Delete a cart by its ID."""
#     return CartService(sess).delete(cart_id)

# ----------------------------------------------------------------------------------------------------------------------

@router.post("/items",
             status_code=status.HTTP_201_CREATED,
             response_model=CartItemRes,
             )
def create_cart_item_route(cart_item: CartItemReq, user: User = Depends(get_user), sess: Session = Depends(sess_db)):
    """
    Create a new CartItem.

    Args:
        cart_item (CartItemReq): Request model for creating a CartItem.
        user (User): The authenticated user.
        sess (Session): SQLAlchemy database session.

    Returns:
        CartItemRes: Response model for a CartItem.
    """
    return CartItemService(sess).insert(cart_item, user)

# @router.get("/items/{cart_item_id}",
#             status_code=status.HTTP_200_OK,
#             response_model=CartItemRes,
#             dependencies=[Security(get_current_user, scopes=["admin"])]
#             )
# def get_cart_item_by_id_route(cart_item_id: UUID, sess: Session = Depends(sess_db)):
#     """Retrieve a cart item by its ID."""
#     return cart_itemservice(sess).get_by_id(cart_item_id)


# @router.get("/items",
#             status_code=status.HTTP_200_OK,
#             response_model=List[CartItemRes],
#             dependencies=[Security(get_current_user, scopes=["admin"])]
#             )
# def get_all_cart_items_route(sess: Session = Depends(sess_db)):
#     """Retrieve all cart items."""
#     cart_items = cart_itemservice(sess).get_all()
#     return cart_items


# @router.patch("/items/{cart_item_id}",
#               status_code=status.HTTP_200_OK,
#               response_model=CartItemRes,
#               )
# def update_cart_item_route(cart_item_id: UUID, cartItem: CartItemUp, user: User = Security(get_user),
#                            sess: Session = Depends(sess_db)):
#     """
#     Partially update a cart item.
#
#     Args:
#         cart_item_id (UUID): UUID of the cart item to be updated.
#         cartItem (CartItemUp): Update model for partially updating a cart item.
#         user (User): The authenticated user.
#         sess (Session): SQLAlchemy database session.
#
#     Returns:
#         CartItemRes: Response model for a cart item.
#     """
#     return cart_itemservice(sess).update(cart_item_id, cartItem, user)


@router.delete("/items/{cart_item_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               )
def delete_cart_item_route(cart_item_id: UUID, user: User = Security(get_user), sess: Session = Depends(sess_db)):
    """
    Delete a CartItem by its ID.

    Args:
        cart_item_id (UUID): UUID of the CartItem to be deleted.
        user (User): The authenticated user.
        sess (Session): SQLAlchemy database session.

    Returns:
        bool: True if the deletion is successful.
    """
    return CartItemService(sess).delete(cart_item_id, user)
