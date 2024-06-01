from fastapi import APIRouter, Depends, Body
from src.db import db
from .schemas import *
from .services import *
from src.auth.models import User
from src.auth.secures import get_admin_user
from ..auth.secures import get_user

router = APIRouter(
    prefix="/super-admin",
    tags=["Super-admin"],
)


@router.get("/24hour-chart", summary="shows all consumptions of devices in recent 24 hours for super admin")
def power_record_24_super_admin(
        user: User = Depends(get_admin_user)
):
    return service_show_records_on_chart_super_admin(
        user_id=user["_id"]
    )


@router.get("/month-chart", summary="shows all consumptions of devices in requested month for super admin")
def power_record_monthly_super_admin(
        year,
        month,
        user: User = Depends(get_admin_user),
):
    return service_show_records_on_chart_monthly_super_admin(
        year=year,
        month=month,
        user_id=user["_id"]
    )


@router.get("/season-chart", summary="shows all consumptions of devices in requested season for super admin")
def power_record_seasonal_super_admin(
        year: int,
        season,
        user: User = Depends(get_admin_user),
):
    return service_show_seasonal_records_on_chart_super_admin(
        year=year,
        season=season,
        user_id=user["_id"]
    )


@router.get("/cal_graph4", summary="shows all consumptions of devices in requested month for super admin")
def cal_unoptimized_super_admin(
        user: User = Depends(get_admin_user),
):
    return service_cal_graph4_super_admin(
        user_id=user["_id"]
    )


@router.get("/all_users", summary="shows all users")
def get_all_users(
        user: User = Depends(get_admin_user),
):
    return service_get_all_user(user_id=user["_id"])
