from src.db import db
from fastapi import Depends, HTTPException
import pymongo
from datetime import datetime
from bson import ObjectId
from .schemas import *
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO


def service_list_power_records(
    user_id: str,
    db
):
    power_records = db["power_records"].find({"user_id": user_id})

    if power_records is None:
        raise HTTPException(status_code=404, detail="Records not found")
    results = []
    for record in power_records:
        record["user_id"] = user_id
        del record["_id"]
        results.append(PowerRecordSchema(**record))
    return results


def service_add_power_records(
    user_id: str,
    power_record: PowerRecordAddSchema,
    db
):
    base_power_record = PowerRecordSchema(
        user_id=user_id,
        device_id=power_record.device_id,
        start_time=power_record.start_time,
        end_time=power_record.end_time
    ).model_dump() # check if it works, dict() is depricated

    update_result = db["power_records"].insert_one(base_power_record)

    return {"detail": "power record added"}

def upload_csv_file(
    file: UploadFile = File(...)
):
    if file.filename.endswith('.csv'):
        df = pd.read_csv(BytesIO(file.read()))
        records = df.to_dict('records')
        result = db["power_records"].insert_many(records)
        
        return JSONResponse(status_code=200, content={"message": f"Inserted {len(result.inserted_ids)} records."})
    else:
        return JSONResponse(status_code=400, content={"message": "Invalid file format. Please upload a .csv file."})
    