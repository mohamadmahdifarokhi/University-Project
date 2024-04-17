from src.db import db
from fastapi import Depends, HTTPException
import pymongo
from datetime import datetime
from bson import ObjectId
from .schemas import *
from fastapi.responses import JSONResponse


def service_add_device(
    device: DeviceSchema,
    db
):
    device = DeviceSchema(
        name=device.name,
        AC_power_consumption=device.AC_power_consumption,
        DC_power_consumption=device.DC_power_consumption
        ).model_dump()

    update_result = db["device"].insert_one(device)

    return {"detail": "device added"}

def service_delete_device(
    device_id: str,
    db
):
    update_result = db["device"].delete_one(
        {"_id": ObjectId(device_id)},
    )
    return {"detail": "device deleted."}


def service_update_device(
    device_id: str,
    device_data: DeviceUpdateSchema,
    db
):
    pass

def service_device_get(
    device_id:str,    
    db
):
    device = db["device"].find_one({"_id": ObjectId(device_id)})
    return device

def service_list_device_all(
    db
):
    devices = db["device"].find()
    results = []
    for device in devices:
        device["id"] = str(device["_id"])
        del device["_id"]
        results.append(DeviceSchema(**device))

    return results

def service_list_device_user(
    user_id: str,
    db
):
    devices = db["users"].find_one({"_id": ObjectId(user_id)})["devices"]
    results = []
    for device_id in devices:
        device = db["device"].find_one({"_id": ObjectId(device_id)})
        device["id"] = str(device["_id"])
        del device["_id"]
        results.append(DeviceSchema(**device))

    return results




















































































