"""Seed realistic, repeatable demo data for the university dashboard.

Usage:
    python -m src.seed_data [email] [password]
"""
import random
import sys
from datetime import datetime, timedelta

from bson import ObjectId

from src.auth.secures import get_password_hash
from src.db.db import db

AREA = 100
DEMO_EMAIL = "user@pardis.ac.ir"
DEMO_PASSWORD = "Demo@12345"

DEVICES = [
    {"name": "لامپ (متوسط)", "size": "medium", "kind": "lamp", "AC_power_consumption": 60.0, "DC_power_consumption": 9.0},
    {"name": "یخچال (متوسط)", "size": "medium", "kind": "appliance", "AC_power_consumption": 150.0, "DC_power_consumption": 120.0},
    {"name": "تلویزیون (متوسط)", "size": "medium", "kind": "appliance", "AC_power_consumption": 110.0, "DC_power_consumption": 90.0},
    {"name": "ماشین لباسشویی (متوسط)", "size": "medium", "kind": "appliance", "AC_power_consumption": 500.0, "DC_power_consumption": 420.0},
    {"name": "کولر گازی (متوسط)", "size": "medium", "kind": "climate", "AC_power_consumption": 1200.0, "DC_power_consumption": 950.0},
    {"name": "بخاری برقی (متوسط)", "size": "medium", "kind": "climate", "AC_power_consumption": 1500.0, "DC_power_consumption": 1200.0},
    {"name": "پمپ آب خورشیدی", "size": "medium", "kind": "appliance", "AC_power_consumption": 370.0, "DC_power_consumption": 300.0},
    {"name": "شارژر خودرو برقی", "size": "medium", "kind": "appliance", "AC_power_consumption": 2200.0, "DC_power_consumption": 1800.0},
]

PRICING = [
    {"season_name": "spring", "general_price": 1100, "peak_price": 2900, "day_light": 13},
    {"season_name": "summer", "general_price": 1425, "peak_price": 3800, "day_light": 14},
    {"season_name": "fall", "general_price": 1100, "peak_price": 2900, "day_light": 11},
    {"season_name": "winter", "general_price": 1250, "peak_price": 3300, "day_light": 10},
]


def ensure_permissions():
    permissions = {}
    for name in ("user", "admin"):
        db["permissions"].update_one(
            {"name": name},
            {"$setOnInsert": {"name": name, "description": name}},
            upsert=True,
        )
        permissions[name] = db["permissions"].find_one({"name": name})
    return permissions


def ensure_demo_user(email, password):
    permissions = ensure_permissions()
    user = db["users"].find_one({"email": email})
    if not user:
        user_id = db["users"].insert_one({
            "email": email,
            "password": get_password_hash(password),
            "provider": "local",
            "permissions": [permissions["user"]],
        }).inserted_id
        user = db["users"].find_one({"_id": user_id})
    else:
        db["users"].update_one(
            {"_id": user["_id"]},
            {"$set": {
                "password": get_password_hash(password),
                "permissions": [permissions["user"]],
                "provider": user.get("provider", "local"),
            }},
        )

    db["profiles"].update_one(
        {"user_id": str(user["_id"])},
        {"$set": {"user_id": str(user["_id"]), "photo": user.get("photo", 7)}},
        upsert=True,
    )
    return user


def ensure_pricing():
    now = datetime(2024, 1, 1)
    for p in PRICING:
        db["pricing"].update_one(
            {"season_name": p["season_name"]},
            {"$set": {
                "season_name": p["season_name"],
                "start_time": now,
                "end_time": now + timedelta(days=90),
                "peak_start_time": now.replace(hour=19),
                "peak_end_time": now.replace(hour=23),
                "general_price": p["general_price"],
                "peak_price": p["peak_price"],
                "day_light": p["day_light"],
            }},
            upsert=True,
        )


def ensure_apartment():
    db["apartments"].update_one(
        {"apartment_no": 1},
        {"$set": {"apartment_no": 1, "admin_id": "system", "block_no": 10}},
        upsert=True,
    )
    return db["apartments"].find_one({"apartment_no": 1})["_id"]


def ensure_block(user_id, apartment_id):
    db["blocks"].update_one(
        {"user_id": str(user_id)},
        {"$set": {"user_id": str(user_id), "apartment_id": str(apartment_id), "unit": 1, "area": str(AREA)}},
        upsert=True,
    )


def ensure_devices(user_id):
    device_ids = []
    for device in DEVICES:
        db["device"].update_one({"name": device["name"]}, {"$set": device}, upsert=True)
        device_ids.append(db["device"].find_one({"name": device["name"]})["_id"])
    db["users"].update_one({"_id": user_id}, {"$set": {"devices": [str(i) for i in device_ids]}})
    return device_ids


def ensure_battery(user_id):
    user = db["users"].find_one({"_id": user_id})
    db["solar_panels"].update_one(
        {"user_id": str(user_id)},
        {"$set": {"user_id": str(user_id), "fee": 17500000, "capacity": 5.5, "status": "active"}},
        upsert=True,
    )
    solar_panel = db["solar_panels"].find_one({"user_id": str(user_id)})
    db["battery"].update_one(
        {"user_id": str(user_id)},
        {"$set": {
            "user_id": str(user_id),
            "solar_panel_id": str(solar_panel["_id"]),
            "saved_energy": 12000,
            "sold_energy": 3000,
            "status": "available",
            "email": user["email"],
            "fee": 50,
            "created_at": datetime.now() - timedelta(days=120),
        }},
        upsert=True,
    )
    return db["battery"].find_one({"user_id": str(user_id)})


def seed_power_records(user_id):
    random.seed(str(user_id))
    db["power_records"].delete_many({"user_id": ObjectId(str(user_id))})
    records = []
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    for day in range(400):
        day_start = now - timedelta(days=day)
        for device in DEVICES:
            for _ in range(random.randint(1, 3)):
                hour = random.randint(5, 22)
                duration_h = random.choice([1, 2, 3, 4])
                start = day_start.replace(hour=hour)
                end = start + timedelta(hours=duration_h)
                consumption = device["DC_power_consumption"] * duration_h
                if device["kind"] == "lamp":
                    consumption *= 6
                records.append({
                    "user_id": ObjectId(str(user_id)),
                    "device_name": device["name"],
                    "start_time": start,
                    "end_time": end,
                    "consumption": round(consumption, 2),
                })
    if records:
        db["power_records"].insert_many(records)
    return len(records)


def main():
    email = sys.argv[1] if len(sys.argv) > 1 else DEMO_EMAIL
    password = sys.argv[2] if len(sys.argv) > 2 else DEMO_PASSWORD
    user = ensure_demo_user(email, password)
    user_id = user["_id"]

    ensure_pricing()
    apartment_id = ensure_apartment()
    ensure_block(user_id, apartment_id)
    ensure_devices(user_id)
    ensure_battery(user_id)
    power_record_count = seed_power_records(user_id)

    print(f"Demo user: {email} / {password}")
    print(f"Seeded {power_record_count} power records.")


if __name__ == "__main__":
    main()
