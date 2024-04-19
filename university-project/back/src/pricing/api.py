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
):
    return service_get_all_pricing(
    )

@router.post("/add", summary="adds pricing")
def pricing_add(
    pricing: PricingSchema,
):
    return service_add_pricing(
        pricing,
    )

@router.delete("/delete", summary="deletes pricing")
def pricing_delete(
    pricing_id: str
):
    return service_delete_pricing(
        pricing_id
    )