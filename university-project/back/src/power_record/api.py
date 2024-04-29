from fastapi import APIRouter, Depends, Body
from src.db import db
from .schemas import *
from .services import *


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