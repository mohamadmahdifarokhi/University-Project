from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from .schemas import (
    OrderResList,
)
from .services import (
    OrderService,
)
from ..auth.models import User
from ..auth.secures import get_current_user
from ..db.db import sess_db

router = APIRouter(tags=["Orders"])


# @router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=OrderRes,
#     responses={
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def create_order_route(
#         order_input: OrderReq,
#         order_service: OrderService = Depends(get_order_service),
# ):
#     """Create a new order."""
#     new_order = order_service.create_order(order_input)
#     print(new_order.__dict__)
#
#     return new_order


# @router.get(
#     "/{orderId}",
#     status_code=status.HTTP_200_OK,
#     response_model=OrderRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Order not found"},
#     },
# )
# def get_order_by_id_route(
#         orderId: UUID,
#         order_service: OrderService = Depends(get_order_service),
# ):
#     """Retrieve an order by its ID."""
#     order = order_service.get_order_by_id(orderId)
#     return order


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=OrderResList,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Orders not found"},
    },
)
def get_orders_by_user_id_route(
        user: User = Depends(get_current_user),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        sess: Session = Depends(sess_db)
):
    """Retrieve orders by user ID with pagination."""
    orders = OrderService(sess).get_by_user_id(user, page, page_size)
    return orders


# @router.patch(
#     "/{orderId}",
#     status_code=status.HTTP_200_OK,
#     response_model=OrderRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Order not found"},
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def update_order_route(
#         orderId: UUID,
#         order_input: OrderUpdate,
#         order_service: OrderService = Depends(get_order_service),
# ):
#     """Partially update an order."""
#     updated_order = order_service.update_order(orderId, order_input)
#     return updated_order


# @router.delete(
#     "/{orderId}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Order not found"},
#     },
# )
# def delete_order_route(
#         orderId: UUID,
#         order_service: OrderService = Depends(get_order_service),
# ):
#     """Delete an order by its ID."""
#     order_service.delete_order(orderId)
#     return None


# @router.post(
#     "/item/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=OrderItemRes,
#     responses={
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def create_orderItem_route(
#         orderItem_input: OrderItemReq,
#         orderItem_service: order_itemservice = Depends(get_orderItem_service),
# ):
#     """Create a new order item."""
#     new_orderItem = orderItem_service.create_orderItem(orderItem_input)
#     return new_orderItem


# @router.get(
#     "/item/{orderItem_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=OrderItemRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Order item not found"},
#     },
# )
# def get_orderItem_by_id_route(
#         orderItem_id: UUID,
#         orderItem_service: order_itemservice = Depends(get_orderItem_service),
# ):
#     """Retrieve an order item by its ID."""
#     orderItem = orderItem_service.get_orderItem_by_id(orderItem_id)
#     print(orderItem.__dict__)
#     return orderItem


# @router.patch(
#     "/item/{orderItem_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=OrderItemRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Order item not found"},
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def update_orderItem_route(
#         orderItem_id: UUID,
#         orderItem_input: OrderItemUpdate,
#         orderItem_service: order_itemservice = Depends(get_orderItem_service),
# ):
#     """Partially update an order item."""
#     updated_orderItem = orderItem_service.update_orderItem(
#         orderItem_id, orderItem_input
#     )
#     return updated_orderItem


# @router.delete(
#     "/item/{orderItem_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Order item not found"},
#     },
# )
# def delete_orderItem_route(
#         orderItem_id: UUID,
#         orderItem_service: order_itemservice = Depends(get_orderItem_service),
# ):
#     """Delete an order item by its ID."""
#     orderItem_service.delete_orderItem(orderItem_id)
#     return None
