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


def _user_display_name(user: dict) -> str | None:
    """Return a human-readable label without exposing a database identifier."""
    for field in ("display_name", "name", "full_name", "username"):
        value = user.get(field)
        if value:
            return str(value)

    first_name = str(user.get("first_name") or "").strip()
    last_name = str(user.get("last_name") or "").strip()
    if first_name or last_name:
        return " ".join(part for part in (first_name, last_name) if part)

    email = user.get("email")
    return str(email) if email else None


def _user_display_names(user_ids) -> dict[str, str]:
    """Build a display-name map for ObjectId and legacy string user references."""
    normalized_ids = {
        str(user_id)
        for user_id in user_ids
        if user_id is not None and str(user_id).strip()
    }
    if not normalized_ids:
        return {}

    object_ids = [
        ObjectId(user_id)
        for user_id in normalized_ids
        if ObjectId.is_valid(user_id)
    ]
    string_ids = [
        user_id for user_id in normalized_ids if not ObjectId.is_valid(user_id)
    ]
    queries = []
    if object_ids:
        queries.append({"_id": {"$in": object_ids}})
    if string_ids:
        queries.append({"_id": {"$in": string_ids}})

    names = {}
    if queries:
        projection = {
            "email": 1,
            "display_name": 1,
            "name": 1,
            "full_name": 1,
            "username": 1,
            "first_name": 1,
            "last_name": 1,
        }
        for user in db["users"].find({"$or": queries}, projection):
            display_name = _user_display_name(user)
            if display_name:
                names[str(user["_id"])] = display_name

    return names


def _decorate_order_user_names(orders: list[dict]) -> list[dict]:
    """Add display labels while keeping raw IDs available for internal actions."""
    user_ids = [
        user_id
        for order in orders
        for user_id in (order.get("user_id"), order.get("seller_id"))
    ]
    names = _user_display_names(user_ids)

    for order in orders:
        buyer_id = str(order.get("user_id")) if order.get("user_id") is not None else ""
        seller_id = str(order.get("seller_id")) if order.get("seller_id") is not None else ""
        order["buyer_name"] = names.get(buyer_id)
        order["seller_name"] = names.get(seller_id)

    return orders


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
    inserted_id = db["orders"].insert_one(base_order).inserted_id
    return {
        "detail": "order added",
        "order_id": str(inserted_id),
        "remaining_energy": updated_battery["saved_energy"],
    }
    
def service_get_order_all(
):
    orders = _decorate_order_user_names(list(db["orders"].find()))
    results = []
    for order in orders:
        order["id"] = str(order["_id"])
        del order["_id"]
        results.append(OrderCreateSchema(**order))

    return results


def service_get_order_buy_user(
    user_id: str,
):
    orders = _decorate_order_user_names(list(db["orders"].find({"user_id": str(user_id)})))
    results = []
    for order in orders:
        order["id"] = str(order["_id"])
        created_at = order.get("created_at")
        order["created_at"] = (
            created_at.isoformat()
            if isinstance(created_at, datetime)
            else str(created_at or "")
        )
        del order["_id"]
        results.append(OrderOutputSchema(**order))
    return results

def service_get_order_sell_user(
    user_id: str,
):
    orders = _decorate_order_user_names(list(db["orders"].find({"seller_id": str(user_id)})))
    results = []
    for order in orders:
        order["id"] = str(order["_id"])
        created_at = order.get("created_at")
        order["created_at"] = (
            created_at.isoformat()
            if isinstance(created_at, datetime)
            else str(created_at or "")
        )
        del order["_id"]
        results.append(OrderOutputSchema(**order))
    return results

def service_delete_order(
    order_id: str,
    user_id,
):
    if not ObjectId.is_valid(str(order_id)):
        raise HTTPException(status_code=404, detail="order not found")
    update_result = db["orders"].delete_one(
        {
            "_id": ObjectId(order_id),
            "$or": [
                {"user_id": str(user_id)},
                {"seller_id": str(user_id)},
            ],
        },
    )
    if update_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="order not found")
    return {"detail": "order deleted."}


def service_last_orders(

):
    orders = _decorate_order_user_names(
        list(db["orders"].find().sort({"created_at": -1}).limit(5))
    )
    results = []
    for order in orders:
        order["id"] = str(order["_id"])
        del order["_id"]
        results.append(OrderCreateSchema(**order))
    return results
