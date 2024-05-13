from fastapi import APIRouter, Depends, Body
from src.db import db
from .schemas import *
from .services import *
from src.auth.models import User
from src.auth.secures import get_current_user
from ..auth.secures import get_user

router = APIRouter(
    prefix="/apartment",
    tags=["Apartments"],
)

@router.get("/", summary="Get an apartment")
def apartment_get(
    apartment_id: str
):
    return service_apartment_get(
        apartment_id
    )

@router.get("/all", summary="Get all apartments")
def battery_list_all(
):
    return service_list_apartment_all(
    )

@router.post("/", summary="adds an apartment")
def device_add(
    apartment: ApartmentSchemacreate,
):
    return service_add_apartment(
        apartment
    )

@router.delete("/", summary="deletes an apartment")
def battery_delete(
    apartment_id: str
):
    return service_delete_apartment(
        apartment_id
    )

