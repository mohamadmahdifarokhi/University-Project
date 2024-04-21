from src.db import db
from fastapi import Depends, HTTPException
import pymongo
from datetime import datetime
from bson import ObjectId
from .schemas import *

def service_add_pricing(
    pricing: PricingSchema,
):
    pricing = PricingSchema(
        device_id=pricing.device_id,
        start_time=pricing.start_time,
        end_time=pricing.end_time,
        price=pricing.price,
        peak_price=pricing.peak_price
        ).model_dump()

    update_result = db["pricing"].insert_one(pricing)

    return {"detail": "pricing added"}

def service_get_all_pricing(
):
    pricings = db["pricing"].find()
    results = []
    for pricing in pricings:
        pricing["id"] = str(pricing["_id"])
        del pricing["_id"]
        results.append(PricingSchema(**pricing))

    return results

def service_get_pricing(
    pricing_id: str,
):
    pricing = db["pricing"].find_one({"_id": ObjectId(pricing_id)})
    return PricingSchema(**pricing)

def service_delete_pricing(
    pricing_id: str,
):
    update_result = db["pricing"].delete_one(
        {"_id": ObjectId(pricing_id)},
    )
    return {"detail": "pricing deleted."}