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

@router.get("/{user_id}", summary="Get all orders of a user")
def devices_list_all_by_user(
    user: User = Depends(get_current_user)
):
    return service_get_order_bu_user(
        user["_id"]
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