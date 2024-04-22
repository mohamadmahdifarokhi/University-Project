
from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session

from .schemas import (
    OrderResList, OrderUpdate, OrderOut, OrderCreate,
)
from .services import (
    OrderService,
)
from ..auth.models import User
from ..auth.secures import get_current_user

router = APIRouter(tags=["Orders"])


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
):
    """Retrieve orders by user ID with pagination."""
    orders = OrderService().get_by_user_id(user, page, page_size)
    return orders

@router.post("/orders/create", response_model=OrderOut)
async def create_order(order: OrderCreate):
    """
    Create a new order.
    """
    return OrderService().create_order(order)

@router.get("/orders/reads")
async def read_orders(skip: int = 0, limit: int = 10):
    """
    Get a list of orders.
    """
    return OrderService().get_orders(skip=skip, limit=limit)

@router.get("/orders/read/{order_id}")
async def read_order(order_id):
    """
    Get an order by ID.
    """
    order = OrderService().get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/orders/update/{order_id}")
async def update_order(order_id, order_update: OrderUpdate):
    """
    Update an order.
    """
    updated_order = OrderService().update_order(order_id, order_update)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/orders/delete/{order_id}")
async def delete_order(order_id):
    """
    Delete an order.
    """
    deleted_order = OrderService().delete_order(order_id)
    if not deleted_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return deleted_order
