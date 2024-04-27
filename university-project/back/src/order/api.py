from fastapi import APIRouter, Depends, Body
from src.db import db
from .schemas import *
from .services import *
from src.auth.models import User
from src.auth.secures import get_current_user


router = APIRouter(
    prefix="/order",
    tags=["Order"],
)


@router.get("/", summary="Get all orders")
def devices_list_all_by_user(
    user: User = Depends(get_current_user)
):
    return service_get_order_all()

@router.get("/buy", summary="Get all selling orders of a user")
def devices_list_all_buy_user(
    user: User = Depends(get_current_user)
):
    return service_get_order_buy_user(
        user["_id"]
    )

@router.get("/sell", summary="Get all buying orders of a user")
def devices_list_all_sell_user(
    user: User = Depends(get_current_user)
):
    return service_get_order_sell_user(
        user["_id"]
    )

@router.get("/last-orders", summary="Get 5 last orders")
def devices_list_last_orders(
):
    return service_last_orders(
    )


@router.post("/", summary="creates an order")
def order_create(
    order: OrderCreateSchema,
):
    return service_create_order(
        order
    )

@router.delete("/", summary="deletes an order by order id")
def devices_list_all_by_user(
    order_id: str,
    user: User = Depends(get_current_user)
):
    return service_delete_order(
        order_id
    )