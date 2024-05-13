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
    apartment = ApartmentSchemacreate(
        apartment_no=apartment_no + 1,
        admin_id=apartment.admin_id,
        block_no=apartment.block_no,
        ).model_dump()

    update_result = db["apartments"].insert_one(apartment)

    return {"detail": "apartment added"}

def service_delete_apartment(
    apartment_id: str,
):
    update_result = db["apartments"].delete_one(
        {"_id": ObjectId(apartment_id)},
    )
    return {"detail": "apartment deleted."}


# def service_update_device(
#     device_id: str,
#     device_data: DeviceUpdateSchema,
# ):
#     pass

def service_apartment_get(
    apartment_id:str,    
):
    apartment = db["apartment"].find_one({"_id": ObjectId(apartment_id)})
    return apartment

def service_list_apartment_all(
):
    apartments = db["apartment"].find()

    results = []
    for apartment in apartments:
        apartment["id"] = str(apartment["_id"])
        del apartment["_id"]
        results.append(ApartmentSchemaGet(**apartment))
    return results



















































































