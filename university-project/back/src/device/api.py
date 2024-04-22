from fastapi import APIRouter, Depends, Body
from src.db import db
from .schemas import *
from .services import *
from src.auth.models import User
from src.auth.secures import get_current_user
from ..auth.secures import get_user

router = APIRouter(
    prefix="/device",
    tags=["Device"],
)

@router.get("/user", summary="Get all devices of a user")
def devices_list_all_by_user(
    user: User = Depends(get_current_user)
):
    return service_list_device_user(
        user["_id"]
    )

@router.get("/", summary="Get all devices")
def devices_list_all(

):
    return service_list_device_all(
    )

@router.post("/add", summary="adds a device")
def device_add(
    device: DeviceSchema,
):
    return service_add_device(
        device
    )

@router.delete("/{device_id}/delete", summary="deletes a device")
def device_delete(
    device_id: str
):
    return service_delete_device(
        device_id
    )

@router.get("/{device_id}/get", summary="gets a device")
def device_get(
    device_id: str
):
    return service_device_get(
        device_id
    )

@router.patch("/select", summary="select device")
async def select_device(
    device_id: str,
    user: User = Depends(get_user)

):
    print(user)
    return service_select_device(
        device_id, user
    )