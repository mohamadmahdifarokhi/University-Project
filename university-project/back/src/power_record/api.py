from fastapi import APIRouter, Depends, Body
from src.db import db
from .schemas import *
from .services import *


router = APIRouter(
    prefix="/power-records",
    tags=["Records"],
)

@router.get("/{user_id}/records", summary="Get all records of a user")
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
        power_record,
        user_id=user["_id"]
    )