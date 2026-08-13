import json
from ..db.db import db
from fastapi import Depends, HTTPException
import pymongo
from datetime import datetime, timedelta
from bson import ObjectId
from .schemas import *
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO
from src.auth.models import User
from src.auth.secures import get_current_user
from datetime import datetime, timedelta
from bson.objectid import ObjectId

def service_list_apartment_blocks(
    apartment_id: str
):
    apartment_id = str(apartment_id)
    apartment_queries = [apartment_id]
    if ObjectId.is_valid(apartment_id):
        apartment_queries.append(ObjectId(apartment_id))
    blocks = db["blocks"].find({"apartment_id": {"$in": apartment_queries}})

    results = []
    for block in blocks:
        user_id = str(block.get("user_id", ""))
        user_query = {"_id": ObjectId(user_id)} if ObjectId.is_valid(user_id) else {"_id": user_id}
        user = db["users"].find_one(user_query)
        base_blocks = BlockSchemaGet(
            id=str(block["_id"]),
            user_id=user.get("email", "") if user else "",
            apartment_id=str(block["apartment_id"]),
            unit=block["unit"],
            area=block["area"]
        ).model_dump()
        results.append(base_blocks)
    return results

def service_delete_block(
        block_id
):
    if not ObjectId.is_valid(str(block_id)):
        raise HTTPException(status_code=404, detail="block not found")
    update_result = db["blocks"].delete_one(
        {"_id": ObjectId(block_id)},
    )
    if update_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="block not found")
    return {"detail": "block_id deleted."}

def service_add_block(
    block: BlockSchemaCreate,
    user_id
):

    apartment = db["apartments"].find_one({"apartment_no": block.apartment_no})
    if apartment is None:
        raise HTTPException(status_code=404, detail="apartment not found")

    apartment_id = apartment["_id"]
    apartment_block_number = apartment["block_no"]
    if block.unit > apartment_block_number:
        raise HTTPException(status_code=400, detail="unit number is not acceptable")
    
    block_check = db["blocks"].find_one({"unit": int(block.unit), "apartment_id": str(apartment_id)})
    if block_check is not None:
        raise HTTPException(status_code=400, detail="this block is not available")

    base_block = BlockSchemaCreate(
        user_id=str(user_id),
        apartment_id=str(apartment_id),
        unit=block.unit,
        area=block.area
    ).model_dump() 

    update_result = db.blocks.insert_one(base_block)

    return {"detail": "block added"}
