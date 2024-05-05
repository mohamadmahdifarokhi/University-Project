from ..db.db import client, db
from fastapi import Depends, HTTPException
import pymongo
from datetime import datetime
from bson import ObjectId
from .schemas import *
from fastapi.responses import JSONResponse
from src.auth.models import User
from src.auth.secures import get_current_user


def service_add_device(
    device: DeviceSchema,
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
    user_id
):
    update_result = db["users"].find_one_and_update(
        {"_id": user_id},
        {"$pull": {"devices": device_id}})
    if update_result:
        return {"detail": "Device deleted successfully."}
    else:
        return {"detail": "User not found or device could not be deleted."}



def service_update_device(
    device_id: str,
    device_data: DeviceUpdateSchema,
):
    pass

def service_device_get(
    device_id:str,    
):
    device = db["device"].find_one({"_id": ObjectId(device_id)})
    return device

def service_list_device_all(
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
):
    devices = db["users"].find_one({"_id": ObjectId(user_id)})["devices"]
    results = []
    print(devices, "loplop")
    for device_id in devices:
        device = db["device"].find_one({"_id": ObjectId(device_id)})
        device["id"] = str(device["_id"])
        del device["_id"]
        results.append(DeviceSchema(**device))

    return results

def service_select_device(
    device_id: str,
user
):
    update_result = db["users"].update_one(
        {
            "_id": ObjectId(user['_id']),
        },
        {
            "$push": {
                "devices": device_id
            },
        },
        upsert=False,
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="user not found")
    return {"detail": "device added."}




















































































