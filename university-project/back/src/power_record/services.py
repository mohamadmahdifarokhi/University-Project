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

def get_season(date):
    month = date.month
    if 3 <= month <= 5:
        return "spring"
    elif 6 <= month <= 8:
        return "summer"
    elif 9 <= month <= 11:
        return "autumn"
    else:
        return "winter"


def service_add_power_records(
    power_record: PowerRecordAddSchema,
    user_id
):
    #calculate consumption due to power of the device
    device = db["device"].find_one({"device_name": power_record.device_name})
    if device and 'dc_power' in device:
        ac_power = device['dc_power']
    time_difference = (power_record['end_time'] - power_record['start_time']).total_seconds() / 3600
    consumption = ac_power * time_difference

    #calculate fee due to the season and time
    record_season = get_season(power_record.start_time)
    pricing_unit = db["pricing"].find_one({"season_name": record_season})


    # if start time is before peak time and duration does not exeed the peak start time
    # if power_record.start_time.time() < pricing_unit["peak_start_time"] and\
    #       (power_record.end_time - power_record.start_time) < (pricing_unit["peak_start_time"] - power_record.start_time.time()):
    #     total_consumption_fee = (power_record.end_time.time() - power_record.start_time.time()) * pricing_unit["general_price"]

    # # 
    # elif power_record.start_time.time() > pricing_unit["peak_start_time"] and power_record.start_time.time() < pricing_unit["peak_end_time"]:
    #     peak_period = (pricing_unit["peak_end_time"] - power_record.start_time.time()).total_seconds() / 3600
    base_power_record = PowerRecordSchema(
        user_id=str(user_id),
        device_name=power_record.device_name,
        start_time=power_record.start_time,
        end_time=power_record.end_time,
        consumption=consumption,
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

# def service_show_records_on_chart(
#     user_id
# ):
#     time_24_hours_ago = datetime.now() - timedelta(days=1)
    
#     query = {
#         "user_id": ObjectId(user_id),
#         "start_time": {"$gte": time_24_hours_ago}
#     }
    
#     user_device_record = db["power_records"].find(query)

#     result = {}

#     for record in user_device_record:
#         device_name = record['device_name']
#         if device_name not in result:
#             result[device_name] = {}

#         duration_seconds = (record['end_time'] - record['start_time']).total_seconds()
#         time_key = record['start_time'] + timedelta(seconds=duration_seconds)
#         time_key_str = time_key.strftime("%Y-%m-%d %H:%M:%S")
        
#         result[device_name][time_key_str] = record['consumption']
    
#     return result



def service_show_records_on_chart(user_id, date=None):
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
                "user_id": ObjectId(str(user_id)),
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
    res = {
        "categories": list(result_dict.keys()),
        "values": list(result_dict.values())
    }

    return res


def service_show_records_on_chart_monthly(user_id, year, month):

    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)

    pipeline = [
        {
            '$match': {
                'user_id': user_id,
                'timestamp': {'$gte': start_date, '$lt': end_date}
            }
        },
        {
            '$group': {
                '_id': {
                    'device_name': '$device_name',
                    'day': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$timestamp'}}
                },
                'total_consumption': {'$sum': '$consumption'}
            }
        },
        {
            '$project': {
                '_id': 0,
                'device_name': '$_id.device_name',
                'date': '$_id.day',
                'total_consumption': 1
            }
        },
        {
            '$sort': {
                'device_name': 1,
                'date': 1
            }
        }
    ]

    results = db["power_records"].aggregate(pipeline)
    categories = sorted({record['date'] for record in results})
    device_data = {}
    for record in results:
        device_name = record['device_name']
        if device_name not in device_data:
            device_data[device_name] = {date: 0 for date in categories}
        device_data[device_name][record['date']] = record['total_consumption']

    formatted_output = [
        {
            'name': device_name,
            'data': [device_data[device_name][date] for date in categories]
        }
        for device_name in sorted(device_data)
    ]

    return formatted_output, categories



def get_season_dates(season, year):
    if season == "Winter":
        start_date = datetime(year, 12, 21)
        end_date = datetime(year + 1, 3, 20)
    elif season == "Spring":
        start_date = datetime(year, 3, 21)
        end_date = datetime(year, 6, 20)
    elif season == "Summer":
        start_date = datetime(year, 6, 21)
        end_date = datetime(year, 9, 22)
    elif season == "Fall":
        start_date = datetime(year, 9, 23)
        end_date = datetime(year, 12, 20)
    else:
        raise ValueError("Invalid season name")
    return start_date, end_date


def service_show_seasonal_records_on_chart(user_id, season, year):
    start_date, end_date = get_season_dates(season, year)
    
    
    pipeline = [
        {
            '$match': {
                'user_id': user_id,
                'start_date': {
                    '$gte': start_date,
                    '$lt': end_date
                }
            }
        },
        {
            '$group': {
                '_id': '$device_name',
                'total_usage': {'$sum': '$consumption'}
            }
        }
    ]
    
    result = list(db["power_records"].aggregate(pipeline))
    
    return result



