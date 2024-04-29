from fastapi import APIRouter, Depends, Body
from src.db import db
from .schemas import *
from .services import *
from src.auth.models import User
from src.auth.secures import get_current_user
from ..auth.secures import get_user

router = APIRouter(
    prefix="/battery",
    tags=["Battery"],
)

@router.get("/", summary="Get battery of a user")
def battery_list_all_by_user(
    user: User = Depends(get_current_user)
):
    return service_battery_by_user_id(
        user["_id"]
    )

@router.get("/all", summary="Get all battery")
def battery_list_all(
):
    return service_list_battery_all(
    )

@router.post("/", summary="adds a battery")
def device_add(
    battery: BatterySchema,
    user: User = Depends(get_current_user)
):
    return service_add_battery(
        battery,
        user["_id"]
    )

@router.delete("/{battery_id}/delete", summary="deletes a battery")
def battery_delete(
    battery_id: str
):
    return service_delete_battery(
        battery_id
    )

@router.get("/{battery_id}", summary="gets a battery by id")
def device_get(
    battery_id: str
):
    return service_battery_get_by_id(
        battery_id
    )
