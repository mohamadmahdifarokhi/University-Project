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
from src.auth.models import User
from src.auth.secures import get_current_user

def service_list_power_records(
    user_id: str,
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
):
    base_power_record = PowerRecordSchema(
        user_id=user_id,
        device_id=power_record.device_name,
        start_time=power_record.start_time,
        end_time=power_record.end_time
    ).model_dump() # check if it works, dict() is depricated

    update_result = db["power_records"].insert_one(base_power_record)

    return {"detail": "power record added"}

def upload_excel_file(file: UploadFile = File(...),
                      user: User = Depends(get_current_user)):
    if not file.filename.endswith('.xlsx'):
        return JSONResponse(status_code=400, content={"message": "Invalid file format. Please upload a .xlsx file."})
    
    # Read the file into a DataFrame
    content = file.read()  
    df = pd.read_excel(BytesIO(content))
    
    expected_columns = ["start_time", "end_time", "AC_or_DC", "consumption"]
    if not all(col in df.columns for col in expected_columns):
        return JSONResponse(status_code=400, content={"message": "Excel file does not have the required columns."})
    
    records = df.to_dict('records')
    for record in records:
        record["user_id"] = user.id
    result = db["power_records"].insert_many(records)
    
    return JSONResponse(status_code=200, content={"message": f"Inserted {len(result.inserted_ids)} records."})