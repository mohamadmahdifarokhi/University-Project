
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from src.db import db
from .schemas import *
from .services import *
from io import BytesIO
import pandas as pd

from ..auth.models import User
from ..auth.secures import get_current_user

router = APIRouter(
    prefix="/power-records",
    tags=["Records"],
)

@router.get("/records", summary="Get all records of a user")
def power_records_list_all(
    user: User = Depends(get_current_user)
):
    return service_list_power_records(
        user_id=user["_id"]
    )

@router.post("/add-record", summary="adds a record to power records with user id")
def power_record_add(
    power_record: PowerRecordAddSchema,
    user: User = Depends(get_current_user)
):
    return service_add_power_records(
        power_record=power_record,
        user_id=user["_id"]
    )


@router.get("/cal8")
def cal8(
    user: User = Depends(get_current_user)
):
    return get_8_cal(
        user_id=user["_id"]
    )


@router.post("/upload-excel-file", summary="Uploads an Excel file containing power records")
async def upload_excel_file(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    if not file.filename.endswith('.xlsx'):
        return JSONResponse(status_code=400, content={"message": "Invalid file format. Please upload a .xlsx file."})

    # Read the file into a DataFrame
    content = await file.read()
    df = pd.read_excel(BytesIO(content))

    expected_columns = ["start_time", "end_time", "device_name"]
    if not all(col in df.columns for col in expected_columns):
        return JSONResponse(status_code=400, content={"message": "Excel file does not have the required columns."})

    records = df.to_dict('records')
    print(user,"wwwwwwwee")
    for record in records:
        print(record)
        record["user_id"] = user['_id']
        record["start_time"] = pd.to_datetime(record["start_time"])
        record["end_time"] = pd.to_datetime(record["end_time"])
        # Calculate consumption
        device = db["device"].find_one({"name": record["device_name"]})
        if device and 'AC_power_consumption' in device:
            ac_power = device['AC_power_consumption']
        else:
            raise HTTPException(404,"Device not found")
        time_difference = (record["end_time"] - record["start_time"]).total_seconds() / 3600
        consumption = ac_power * time_difference
        record["consumption"] = consumption

        # Calculate fee (if necessary)
        # record_season = get_season(record["start_time"])
        # pricing_unit = db["pricing"].find_one({"season_name": record_season})
        # if pricing_unit:
        #     # Add logic for fee calculation based on pricing_unit
        #     pass

    result = db["power_records"].insert_many(records)

    return JSONResponse(status_code=200, content={"message": f"Inserted {len(result.inserted_ids)} records."})

@router.delete("/delete-record", summary="deletes a record from power records for a user")
def power_record_delete(
    power_record_id: str,
    user: User = Depends(get_current_user)

):
    return service_delete_power_records(
        power_record_id
    )


@router.get("/24hour-chart", summary="shows all consumptions of devices in recent 24 hours")
def power_record_24(
    user: User = Depends(get_current_user)
):
    return service_show_records_on_chart(
        user_id=user["_id"]
    )


@router.get("/month-chart", summary="shows all consumptions of devices in requested month")
def power_record_monthly(
    year,
    month,
    user: User = Depends(get_current_user),
):
    return service_show_records_on_chart_monthly(
        year=year,
        month=month,
        user_id=user["_id"]
    )


@router.get("/season-chart", summary="shows all consumptions of devices in requested season")
def power_record_seasonal(
    year:int,
    season,
    user: User = Depends(get_current_user),
):
    return service_show_seasonal_records_on_chart(
        year=year,
        season=season,
        user_id=user["_id"]
    )