"""Seed realistic demo data for the complete university application.

Usage (inside backend container):
    python -m src.seed_data "$DEMO_USER_EMAIL"
    python -m src.seed_data --all
"""
import sys
import random
import os
from datetime import datetime, timedelta

from bson import ObjectId

from src.db.db import db
from src.auth.secures import get_password_hash
from src.core.utils import default_user_name

AREA = 100  # valid values used by the calculations: 80, 100, 120
DEMO_USER_EMAIL = os.getenv("DEMO_USER_EMAIL")
DEMO_USER_PASSWORD = os.getenv("DEMO_USER_PASSWORD")

# Devices with Persian names; "size" drives the peak/area calculations,
# and "kind" lets the math identify lamps / climate devices reliably.
DEVICES = [
    {"name": "لامپ (متوسط)", "size": "medium", "kind": "lamp",
     "AC_power_consumption": 60.0, "DC_power_consumption": 9.0},
    {"name": "یخچال (متوسط)", "size": "medium", "kind": "appliance",
     "AC_power_consumption": 150.0, "DC_power_consumption": 120.0},
    {"name": "تلویزیون (متوسط)", "size": "medium", "kind": "appliance",
     "AC_power_consumption": 110.0, "DC_power_consumption": 90.0},
    {"name": "ماشین لباسشویی (متوسط)", "size": "medium", "kind": "appliance",
     "AC_power_consumption": 500.0, "DC_power_consumption": 420.0},
    {"name": "کولر گازی (متوسط)", "size": "medium", "kind": "climate",
     "AC_power_consumption": 1200.0, "DC_power_consumption": 950.0},
    {"name": "بخاری برقی (متوسط)", "size": "medium", "kind": "climate",
     "AC_power_consumption": 1500.0, "DC_power_consumption": 1200.0},
]

PRICING = [
    {"season_name": "spring", "general_price": 1200, "peak_price": 2400, "day_light": 13},
    {"season_name": "summer", "general_price": 1500, "peak_price": 3000, "day_light": 14},
    {"season_name": "fall",   "general_price": 1200, "peak_price": 2400, "day_light": 11},
    {"season_name": "winter", "general_price": 1000, "peak_price": 2000, "day_light": 10},
]


def ensure_demo_user():
    """Keep the documented demo login available for end-to-end UI tests."""
    if not DEMO_USER_EMAIL or not DEMO_USER_PASSWORD:
        raise RuntimeError(
            "Set DEMO_USER_EMAIL and DEMO_USER_PASSWORD in the local environment before seeding."
        )

    user = db["users"].find_one({"email": DEMO_USER_EMAIL})
    if user:
        return user["_id"]
    permission = db["permissions"].find_one({"name": "user"})
    if not permission:
        permission_id = db["permissions"].insert_one(
            {"name": "user", "description": "user"}
        ).inserted_id
        permission = db["permissions"].find_one({"_id": permission_id})
    user_id = db["users"].insert_one({
        "email": DEMO_USER_EMAIL,
        "name": default_user_name(DEMO_USER_EMAIL),
        "password": get_password_hash(DEMO_USER_PASSWORD),
        "permissions": [permission],
        "devices": [],
        "is_active": True,
    }).inserted_id
    print(f"demo user created: {user_id}")
    return user_id


def ensure_pricing():
    for p in PRICING:
        if not db["pricing"].find_one({"season_name": p["season_name"]}):
            now = datetime(2024, 1, 1)
            db["pricing"].insert_one({
                "season_name": p["season_name"],
                "start_time": now,
                "end_time": now + timedelta(days=90),
                "peak_start_time": now.replace(hour=19),
                "peak_end_time": now.replace(hour=23),
                "general_price": p["general_price"],
                "peak_price": p["peak_price"],
                "day_light": p["day_light"],
            })
    print("pricing ready")


def ensure_apartment():
    apt = db["apartments"].find_one({"apartment_no": 1})
    if not apt:
        apt_id = db["apartments"].insert_one({
            "apartment_no": 1,
            "admin_id": "system",
            "block_no": 10,
        }).inserted_id
        print(f"apartment created: {apt_id}")
        return apt_id
    print("apartment exists")
    return apt["_id"]


def ensure_block(user_id, apartment_id):
    block = db["blocks"].find_one({"user_id": str(user_id)})
    if not block:
        db["blocks"].insert_one({
            "user_id": str(user_id),
            "apartment_id": str(apartment_id),
            "unit": 1,
            "area": str(AREA),
        })
        print("block created")
    else:
        db["blocks"].update_one({"_id": block["_id"]}, {"$set": {"area": str(AREA)}})
        print("block updated")


def ensure_profile(user_id):
    profile = db["profiles"].find_one({"user_id": str(user_id)})
    if not profile:
        db["profiles"].insert_one({"user_id": str(user_id), "photo": 1})
        print("profile created")
    else:
        print("profile exists")


def ensure_cart(user_id, product_ids=None):
    """Ensure every account has a cart so shop/cart screens are populated safely."""
    cart = db["carts"].find_one({"user_id": str(user_id)})
    if not cart:
        db["carts"].insert_one({"user_id": str(user_id), "cart_items": []})
        print("cart created")
        cart = {"cart_items": []}

    # Populate only empty demo carts; never overwrite a user's existing cart.
    if product_ids and not cart.get("cart_items"):
        db["carts"].update_one(
            {"user_id": str(user_id)},
            {"$set": {"cart_items": [
                {"product_id": str(product_ids[0]), "count": 1},
                {"product_id": str(product_ids[1]), "count": 1},
            ]}},
        )
        print("demo cart populated")


def ensure_devices(user_id):
    device_ids = []
    for d in DEVICES:
        existing = db["device"].find_one({"name": d["name"]})
        if existing:
            db["device"].update_one({"_id": existing["_id"]}, {"$set": d})
            device_ids.append(existing["_id"])
        else:
            device_ids.append(db["device"].insert_one(dict(d)).inserted_id)
    # link devices to the user (string ids, as service_select_device does)
    db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"devices": [str(i) for i in device_ids]}},
    )
    print(f"{len(device_ids)} devices ready and linked to user")
    return device_ids


def ensure_battery(user_id):
    user = db["users"].find_one({"_id": ObjectId(user_id)})
    existing = db["battery"].find_one({"user_id": str(user_id)})
    if existing:
        updates = {
            "status": "available",
            "email": user["email"],
            "fee": 50,
        }
        if not existing.get("created_at"):
            updates["created_at"] = datetime.now() - timedelta(days=120)
        if not existing.get("saved_energy"):
            updates["saved_energy"] = 12000
        db["battery"].update_one({"_id": existing["_id"]}, {"$set": updates})
        print("battery updated")
        return existing["_id"]
    solar = db["solar_panels"].find_one({"user_id": str(user_id)})
    sp_id = solar["_id"] if solar else db["solar_panels"].insert_one(
        {"user_id": str(user_id), "fee": 0}
    ).inserted_id
    battery_id = db["battery"].insert_one({
        "user_id": str(user_id),
        "solar_panel_id": str(sp_id),
        "saved_energy": 12000,
        "sold_energy": 3000,
        "status": "available",
        "email": user["email"],
        "fee": 50,
        "created_at": datetime.now() - timedelta(days=120),
    }).inserted_id
    print("battery + solar panel created")
    return battery_id


def seed_power_records(user_id):
    # Replace only records generated by this seed; preserve imported/backup data.
    db["power_records"].delete_many({
        "user_id": ObjectId(str(user_id)),
        "mock": True,
    })
    records = []
    now = datetime.now()
    # One complete year keeps every seasonal dashboard comparison populated.
    for day in range(365):
        day_start = now - timedelta(days=day)
        for d in DEVICES:
            sessions = random.randint(1, 3)
            for _ in range(sessions):
                hour = random.randint(6, 22)
                duration_h = random.choice([1, 2, 3])
                start = day_start.replace(hour=hour, minute=0, second=0, microsecond=0)
                end = start + timedelta(hours=duration_h)
                consumption = d["DC_power_consumption"] * duration_h
                if d.get("kind") == "lamp":
                    consumption *= 6
                records.append({
                    # IMPORTANT: store user_id as ObjectId so chart aggregations match
                    "user_id": ObjectId(str(user_id)),
                    "device_name": d["name"],
                    "start_time": start,
                    "end_time": end,
                    "consumption": round(consumption, 2),
                    "mock": True,
                })
    db["power_records"].insert_many(records)
    print(f"{len(records)} power records created")


def seed_shop():
    # Categories
    categories = [
        {"name": {"fa": "پنل خورشیدی", "en": "Solar Panel"}},
        {"name": {"fa": "باتری", "en": "Battery"}},
        {"name": {"fa": "اینورتر", "en": "Inverter"}},
    ]
    cat_ids = {}
    for c in categories:
        existing = db["categories"].find_one({"name.en": c["name"]["en"]})
        if existing:
            cat_ids[c["name"]["en"]] = existing["_id"]
        else:
            cat_ids[c["name"]["en"]] = db["categories"].insert_one(dict(c)).inserted_id

    products = [
        {
            "slug": "solar-panel-450w",
            "name": {"fa": "پنل خورشیدی ۴۵۰ وات", "en": "Solar Panel 450W"},
            "description": {"fa": "پنل خورشیدی مونوکریستال ۴۵۰ وات", "en": "450W monocrystalline solar panel"},
            "price": 12000000,
            "logo": "/img/flashlight-line.png",
            "photo": "/img/azad-pardis-logo.png",
            "background": "/img/164.png",
            "isActivate": True,
            "category_id": str(cat_ids["Solar Panel"]),
        },
        {
            "slug": "lithium-battery-5kwh",
            "name": {"fa": "باتری لیتیومی ۵ کیلووات‌ساعت", "en": "Lithium Battery 5kWh"},
            "description": {"fa": "باتری ذخیره‌ساز انرژی ۵ کیلووات‌ساعت", "en": "5kWh energy storage battery"},
            "price": 35000000,
            "logo": "/img/battery-saver-line.png",
            "photo": "/img/azad-pardis-logo.png",
            "background": "/img/164.png",
            "isActivate": True,
            "category_id": str(cat_ids["Battery"]),
        },
        {
            "slug": "hybrid-inverter-3kw",
            "name": {"fa": "اینورتر هیبرید ۳ کیلووات", "en": "Hybrid Inverter 3kW"},
            "description": {"fa": "اینورتر هیبرید خورشیدی ۳ کیلووات", "en": "3kW hybrid solar inverter"},
            "price": 22000000,
            "logo": "/img/exchange-line.png",
            "photo": "/img/azad-pardis-logo.png",
            "background": "/img/164.png",
            "isActivate": True,
            "category_id": str(cat_ids["Inverter"]),
        },
        {
            "slug": "smart-meter",
            "name": {"fa": "کنتور هوشمند", "en": "Smart Meter"},
            "description": {"fa": "کنتور هوشمند پایش مصرف", "en": "Smart consumption metering device"},
            "price": 4500000,
            "logo": "/img/speed-up-line.svg",
            "photo": "/img/azad-pardis-logo.png",
            "background": "/img/164.png",
            "isActivate": False,
            "category_id": str(cat_ids["Inverter"]),
        },
    ]
    product_ids = []
    for p in products:
        existing = db["products"].find_one({"slug": p["slug"]})
        if existing:
            product_ids.append(existing["_id"])
        else:
            product_ids.append(db["products"].insert_one(dict(p)).inserted_id)
    print(f"{len(categories)} categories, {len(products)} products ready")
    return product_ids


def seed_orders(users):
    """Create deterministic buy/sell history between demo users."""
    if len(users) < 2:
        print("orders skipped: at least two users are required")
        return
    db["orders"].delete_many({"mock": True})
    orders = []
    for index in range(8):
        buyer = users[index % len(users)]
        seller = users[(index + 1) % len(users)]
        battery = db["battery"].find_one({"user_id": str(seller["_id"])})
        if not battery:
            continue
        amount = 100 + index * 25
        orders.append({
            "user_id": str(buyer["_id"]),
            "battery_id": str(battery["_id"]),
            "seller_id": str(seller["_id"]),
            "amount": amount,
            "fee": amount * int(battery.get("fee", 50)),
            "created_at": datetime.now() - timedelta(days=index * 3 + 1),
            "mock": True,
        })
    if orders:
        db["orders"].insert_many(orders)
    print(f"{len(orders)} mock orders created")


def main():
    ensure_pricing()
    apt_id = ensure_apartment()
    ensure_demo_user()
    target = sys.argv[1] if len(sys.argv) > 1 else "--all"
    users = list(db["users"].find()) if target == "--all" else list(
        db["users"].find({"email": target})
    )
    if not users:
        print(f"No users found for target: {target}")
        return
    for unit, user in enumerate(users, start=1):
        user_id = user["_id"]
        print(f"Seeding data for {user['email']} ({user_id})")
        ensure_profile(user_id)
        ensure_cart(user_id)
        ensure_block(user_id, apt_id)
        ensure_devices(user_id)
        ensure_battery(user_id)
        seed_power_records(user_id)
        db["blocks"].update_one(
            {"user_id": str(user_id)},
            {"$set": {"unit": unit, "area": str(AREA)}},
        )
    product_ids = seed_shop()
    for user in users:
        ensure_cart(user["_id"], product_ids)
    seed_orders(users)
    print("DONE")


if __name__ == "__main__":
    main()
