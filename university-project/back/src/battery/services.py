from ..db.db import client, db
from fastapi import Depends, HTTPException
import pymongo
from datetime import datetime
from bson import ObjectId
from .schemas import *
from fastapi.responses import JSONResponse
from src.auth.models import User
from src.auth.secures import get_current_user


def service_add_battery(
    battery: BatterySchema,
    user_id: str
):  
    user_battery = db["battery"].find_one({"user_id": user_id})
    solar_panel_id = db["solar_panels"].find_one({"user_id": str(user_id)})["_id"]

    if user_battery is not None:
        raise HTTPException(status_code=403, detail="This user has a battery") 
    battery = BatterySchema(
        user_id=str(user_id),
        solar_panel_id=str(solar_panel_id),
        saved_energy=battery.saved_energy,
        sold_energy=battery.sold_energy
        ).model_dump()

    update_result = db["battery"].insert_one(battery)

    return {"detail": "battery added"}

def service_delete_battery(
    battery_id: str,
):
    update_result = db["battery"].delete_one(
        {"_id": ObjectId(battery_id)},
    )
    return {"detail": "battery deleted."}


# def service_update_device(
#     device_id: str,
#     device_data: DeviceUpdateSchema,
# ):
#     pass

def service_battery_get_by_id(
    battery_id:str,    
):
    battery = db["battery"].find_one({"_id": ObjectId(battery_id)})
    return battery

def service_list_battery_all(
):
    battery = db["battery"].find()

    results = []
    for battery in battery:
        user = db["users"].find_one({"_id": ObjectId(battery['user_id'])})

        battery["id"] = str(battery["_id"])
        battery["email"] = str(user["email"])
        battery["status"] = 'available'
        del battery["_id"]
        results.append(BatterySchema(**battery))

    return results

def service_battery_by_user_id(
    user_id: str,
):
    battery = db["battery"].find_one({"user_id": str(user_id)})
    battery["id"] = str(battery["_id"])
    del battery["_id"]

    return BatterySchema(**battery)

















































































