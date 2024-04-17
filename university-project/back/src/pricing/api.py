from fastapi import APIRouter, Depends, Body
from src.db import db
from .schemas import *
from .services import *


router = APIRouter(
    prefix="/pricing",
    tags=["Pricing"],
)

@router.get("/", summary="Get all pricings")
def pricing_list_all(
    db=db
):
    return service_get_all_pricing(
        db=db
    )

@router.post("/add", summary="adds pricing")
def pricing_add(
    pricing: PricingSchema,
    db=db
):
    return service_add_pricing(
        pricing,
        db=db,
    )

@router.delete("/delete", summary="deletes pricing")
def pricing_delete(
    pricing_id: str,
    db=db
):
    return service_delete_pricing(
        pricing_id,
        db=db,
    )