from bson import ObjectId
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.db import db
from .models import Order
from .schemas import *
from ..auth.models import User

from typing import Optional, List

from pymongo import MongoClient
from fastapi import HTTPException, status
from datetime import datetime
from .models import Order
from .schemas import OrderOut, OrderCreate, OrderUpdate
from ..db.db import db
from ..logger import logger
# from ..product.models import Product
from datetime import datetime

from pydantic_mongo import ObjectIdField
from bson import ObjectId
from pymongo import ReturnDocument


def service_create_order(
    order: OrderCreateSchema,
    user_id
):
    try:
        battery_object_id = ObjectId(order.battery_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid battery id.")

    battery = db["battery"].find_one({"_id": battery_object_id})
    if battery is None:
        raise HTTPException(status_code=404, detail="Battery not found.")

    if order.amount <= 0:
        raise HTTPException(status_code=400, detail="Order amount must be positive.")

    if str(battery["user_id"]) == str(user_id):
        raise HTTPException(status_code=400, detail="You cannot buy your own energy.")

    updated_battery = db["battery"].find_one_and_update(
        {
            "_id": battery_object_id,
            "saved_energy": {"$gte": order.amount},
        },
        {
            "$inc": {
                "saved_energy": -order.amount,
                "sold_energy": order.amount,
            },
        },
        return_document=ReturnDocument.AFTER,
    )
    if updated_battery is None:
        raise HTTPException(status_code=400, detail="Insufficient saved energy.")

    seller_id = battery["user_id"]
    base_order = OrderCreateSchema(
        user_id=str(user_id),
        battery_id=order.battery_id,
        seller_id=seller_id,
        amount=order.amount,
        fee=order.amount*50,
        created_at=datetime.now()
    ).model_dump()
    db["orders"].insert_one(base_order)
    return {
        "detail": "order added",
        "order_id": str(base_order.get("_id", "")),
        "remaining_energy": updated_battery["saved_energy"],
    }
    
def service_get_order_all(
):
    orders = db["orders"].find()
    results = []
    for order in orders:
        order["id"] = str(order["_id"])
        del order["_id"]
        results.append(OrderCreateSchema(**order))

    return results


def service_get_order_buy_user(
    user_id: str,
):
    orders = db["orders"].find({"user_id": str(user_id)})
    results = []
    for order in orders:
        order["id"] = str(order["_id"])
        created_at = order.get("created_at")
        order["created_at"] = (
            created_at.strftime("%d-%b-%Y")
            if isinstance(created_at, datetime)
            else str(created_at or "")
        )
        del order["_id"]
        results.append(OrderOutputSchema(**order))
    return results

def service_get_order_sell_user(
    user_id: str,
):
    orders = db["orders"].find({"seller_id": str(user_id)})
    results = []
    for order in orders:
        order["id"] = str(order["_id"])
        created_at = order.get("created_at")
        order["created_at"] = (
            created_at.strftime("%d-%b-%Y")
            if isinstance(created_at, datetime)
            else str(created_at or "")
        )
        del order["_id"]
        results.append(OrderOutputSchema(**order))
    return results

def service_delete_order(
    order_id: str,
):
    update_result = db["orders"].delete_one(
        {"_id": ObjectId(order_id)},
    )
    return {"detail": "order deleted."}


def service_last_orders(

):
    orders = db["orders"].find().sort({"created_at": -1}).limit(5)
    results = []
    for order in orders:
        order["id"] = str(order["_id"])
        del order["_id"]
        results.append(OrderCreateSchema(**order))
    return results
