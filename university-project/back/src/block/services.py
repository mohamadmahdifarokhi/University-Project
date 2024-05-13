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
    blocks = db["blocks"].find({"apartment_id": ObjectId(apartment_id)})

    if blocks is None:
        raise HTTPException(status_code=404, detail="apartment not found")
    results = []
    for block in blocks:
        user_name = db["users"].find_one({"_id": ObjectId(block["user_id"])})["email"]
        if user_name is None:
            raise HTTPException(status_code=404, detail="user not found")
        base_blocks = BlockSchemaGet(
        blocks_id=str(block["_id"]),
        user_id=user_name,
        apartment_id=block["apartment_id"],
        unit=block["unit"],
        area=block["area"]
    ).model_dump()
        results.append(base_blocks)
    return results

def service_delete_block(
        block_id
):
    update_result = db["blocks"].delete_one(
        {"_id": ObjectId(block_id)},
    )
    return {"detail": "block_id deleted."}

def service_add_block(
    block: BlockSchemaCreate,
    user_id
):

    apartment_id = db["apartments"].find_one({"apartment_no": (block.apartment_no)})["_id"]
    if apartment_id is None:
        raise HTTPException(status_code=404, detail="apartment not found")
    
    apartment_block_number = db["apartments"].find_one({"_id": apartment_id})["block_no"]
    if block.unit > apartment_block_number:
        raise HTTPException(status_code=400, detail="unit number is not acceptable")
    
    block_check = db["blocks"].find_one({"unit": int(block.unit), "apartment_id": str(apartment_id)})
    print(block_check)
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

