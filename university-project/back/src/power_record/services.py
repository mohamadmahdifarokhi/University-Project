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

def service_list_power_records(
    user_id: str
):
    power_records = db["power_records"].find({"user_id": user_id})

    if power_records is None:
        raise HTTPException(status_code=404, detail="Records not found")
    results = []
    for record in power_records:
        base_power_record = PowerRecordGetSchema(
        power_record_id=str(record["_id"]),
        device_name=record["device_name"],
        start_time=record["start_time"],
        end_time=record["end_time"],
        consumption=record["consumption"],
    ).model_dump()
        results.append(base_power_record)
    return results

def service_delete_power_records(
        power_record_id
):
    update_result = db["power_records"].delete_one(
        {"_id": ObjectId(power_record_id)},
    )
    return {"detail": "power record deleted."}

def service_add_power_records(
    power_record: PowerRecordAddSchema,
    user_id
):
    base_power_record = PowerRecordSchema(
        user_id=str(user_id),
        device_name=power_record.device_name,
        start_time=power_record.start_time,
        end_time=power_record.end_time,
        consumption=power_record.consumption
    ).model_dump() # check if it works, dict() is depricated

    update_result = db.power_records.insert_one(base_power_record)

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

def service_show_records_on_chart(
    user_id
):
    time_24_hours_ago = datetime.now() - timedelta(days=1)
    
    query = {
        "user_id": ObjectId(user_id),
        "start_time": {"$gte": time_24_hours_ago}
    }
    
    user_device_record = db["power_records"].find(query)

    result = {}

    for record in user_device_record:
        device_name = record['device_name']
        if device_name not in result:
            result[device_name] = {}

        duration_seconds = (record['end_time'] - record['start_time']).total_seconds()
        time_key = record['start_time'] + timedelta(seconds=duration_seconds)
        time_key_str = time_key.strftime("%Y-%m-%d %H:%M:%S")
        
        result[device_name][time_key_str] = record['consumption']
    
    return result

    
from datetime import datetime, timedelta
from bson.objectid import ObjectId

def service_show_records_on_chart(db, user_id, date=None):
    if date is None:
        date = datetime.now().date()
    else:
        date = datetime.strptime(date, '%Y-%m-%d').date()

    start_time = datetime.combine(date, datetime.min.time())
    end_time = datetime.combine(date, datetime.max.time())

    # Aggregation pipeline to sum up consumption for each device
    pipeline = [
        {
            "$match": {
                "user_id": ObjectId(user_id),
                "start_time": {"$gte": start_time, "$lt": end_time}
            }
        },
        {
            "$group": {
                "_id": "$device_name",  # Group by device name
                "total_consumption": {"$sum": "$consumption"}  # Sum up consumption
            }
        },
        {
            "$project": {
                "_id": 0,
                "device_name": "$_id",
                "total_consumption": 1
            }
        }
    ]

    results = db["power_records"].aggregate(pipeline)
    result_dict = {doc["device_name"]: doc["total_consumption"] for doc in results}

    return result_dict