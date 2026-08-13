from ..db.db import client, db
from fastapi import Depends, HTTPException
import pymongo
from datetime import datetime
from bson import ObjectId
from .schemas import *
from fastapi.responses import JSONResponse
from src.auth.models import User
from src.auth.secures import get_current_user


def service_add_apartment(
    apartment: ApartmentSchemacreate,
):  
    apartment_no = db["apartments"].count_documents({})
    apartment = ApartmentSchemaGet(
        apartment_no=apartment_no + 1,
        admin_id=apartment.admin_id,
        block_no=apartment.block_no,
        ).model_dump()

    update_result = db["apartments"].insert_one(apartment)

    return {"detail": "apartment added"}

def service_delete_apartment(
    apartment_id: str,
):
    if not ObjectId.is_valid(str(apartment_id)):
        raise HTTPException(status_code=404, detail="apartment not found")
    update_result = db["apartments"].delete_one(
        {"_id": ObjectId(apartment_id)},
    )
    if update_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="apartment not found")
    return {"detail": "apartment deleted."}


# def service_update_device(
#     device_id: str,
#     device_data: DeviceUpdateSchema,
# ):
#     pass

def service_apartment_get(
    apartment_id:str,    
):
    if not ObjectId.is_valid(str(apartment_id)):
        raise HTTPException(status_code=404, detail="apartment not found")
    apartment = db["apartments"].find_one({"_id": ObjectId(apartment_id)})
    if apartment is None:
        raise HTTPException(status_code=404, detail="apartment not found")
    apartment["id"] = str(apartment.pop("_id"))
    return apartment

def service_list_apartment_all(
    user_id: str,
):
    results = []
    for block in db["blocks"].find({"user_id": str(user_id)}):
        apartment_id = str(block.get("apartment_id", ""))
        if not ObjectId.is_valid(apartment_id):
            continue
        apartment = db["apartments"].find_one({"_id": ObjectId(apartment_id)})
        if not apartment:
            continue
        results.append({
            "id": str(apartment["_id"]),
            "apartment_no": apartment.get("apartment_no"),
            "admin_id": apartment.get("admin_id"),
            "block_no": apartment.get("block_no"),
            "unit": block.get("unit"),
            "area": block.get("area"),
        })
    return results


def service_list_available_apartments():
    return [
        {
            "id": str(apartment["_id"]),
            "apartment_no": apartment.get("apartment_no"),
            "block_no": apartment.get("block_no"),
        }
        for apartment in db["apartments"].find(
            {},
            {"apartment_no": 1, "block_no": 1},
        ).sort("apartment_no", 1)
    ]
















































































