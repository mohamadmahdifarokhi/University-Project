from fastapi import APIRouter, Depends, Body
from src.db import db
from .schemas import *
from .services import *


router = APIRouter(
    prefix="/device",
    tags=["Device"],
)

@router.get("/{user_id}/devices", summary="Get all devices of a user")
def devices_list_all(
    user_id: str
):
    return service_list_device_user(
        user_id=user_id
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