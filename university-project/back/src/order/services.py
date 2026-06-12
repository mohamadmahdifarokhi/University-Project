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


def service_create_order(
    order: OrderCreateSchema,
    user_id
):
    battery = db["battery"].find_one({"_id": ObjectId(order.battery_id)})
    if battery is None:
        raise HTTPException(status_code=404, detail="Battery not found.")

    if battery["saved_energy"] < order.amount:
        raise HTTPException(status_code=400, detail="Insufficient saved energy.")
    
    seller_id = db["battery"].find_one({"_id": ObjectId(order.battery_id)})["user_id"]
    base_order = OrderCreateSchema(
        user_id=str(user_id),
        battery_id=order.battery_id,
        seller_id=seller_id,
        amount=order.amount,
        fee=order.amount*50,
        created_at=str(datetime.now())
    ).model_dump()
    db["orders"].insert_one(base_order)
    update_result = db["battery"].update_one(
        {
            "_id": ObjectId(order.battery_id),
        },
        {
            "$set": {
                "saved_capacity": battery["saved_energy"] - order.amount,
                "sold_capacity": battery["sold_energy"] + order.amount,
            },
        },
        upsert=False,
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Battery not found")
    return {"detail": "order added"}
    
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
        order["created_at"] = order["created_at"].strftime("%d-%b-%Y")
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
        order["created_at"] = order["created_at"].strftime("%d-%b-%Y")
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
