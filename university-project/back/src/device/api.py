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
    user_id: str,
    db=db
):
    return service_list_device_user(
        db=db, user_id=user_id
    )

@router.get("/", summary="Get all devices")
def devices_list_all(
    db=db
):
    return service_list_device_all(
        db=db
    )

@router.post("/add", summary="adds a device")
def device_add(
    device: DeviceSchema,
    db=db
):
    return service_add_device(
        device,
        db=db,
    )

@router.delete("/{device_id}/delete", summary="deletes a device")
def device_delete(
    device_id: str,
    db=db
):
    return service_delete_device(
        device_id,
        db=db,
    )

@router.get("/{device_id}/get", summary="gets a device")
def device_get(
    device_id: str,
    db=db
):
    return service_device_get(
        device_id,
        db=db,
    )