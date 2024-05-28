from ..db.db import client, db
from fastapi import Depends, HTTPException
import pymongo
from datetime import datetime, timedelta
from bson import ObjectId
from .schemas import BatterySchema, BatteryAddSchema
from fastapi.responses import JSONResponse
from src.auth.models import User
from src.auth.secures import get_current_user


def service_add_battery(
    battery: BatterySchema,
    user_id: str
):  
    email = db["users"].find_one({"_id": ObjectId(user_id)})["email"]
    user_battery = db["battery"].find_one({"user_id": user_id})
    solar_panel_id = db["solar_panels"].find_one({"user_id": str(user_id)})["_id"]

    if user_battery is not None:
        raise HTTPException(status_code=403, detail="This user has a battery")

    battery = BatterySchema(
        user_id=str(user_id),
        solar_panel_id=str(solar_panel_id),
        saved_energy=battery.saved_energy,
        sold_energy=battery.sold_energy,
        email=email,
        created_at=datetime.now(),
        ).model_dump()

    update_result = db["battery"].insert_one(battery)

    return {"detail": "battery added"}

def service_delete_battery(
    battery_id: str,
):
    update_result = db["battery"].delete_one(
        {"_id": ObjectId(battery_id)},
    )
    return {"detail": "battery deleted."}


# def service_update_device(
#     device_id: str,
#     device_data: DeviceUpdateSchema,
# ):
#     pass

def service_battery_get_by_id(
    battery_id:str,    
):
    battery = db["battery"].find_one({"_id": ObjectId(battery_id)})
    return battery

def service_list_battery_all(
):
    get_all_season = db["pricing"].find()
    daylights = {}
    for season in get_all_season:
        daylights[season["season_name"]] = season["day_light"]

    batteries = db["battery"].find()
    for battery in batteries:
        # update battery saving
        current_date = datetime.now()
        created_at = battery["created_at"]
        periods = divide_into_periods(created_at, current_date)

        total_daylight_saving = 0
        for period in periods:
            season = period['season']
            start = period['start']
            end = period['end']
            num_days = (end - start).days + 1
            daylight = daylights.get(season, 0)  # Default to 0 if the season is not found
            total_daylight_saving += (num_days * daylight) * 50
        update_result = db["battery"].update_one(
        {
            "_id": battery["_id"],
        },
        {
            "$set": {
                "saved_energy": total_daylight_saving
            },
        },
        upsert=False,
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="battery not found")

    results = []
    for battery in batteries:
        user = db["users"].find_one({"_id": ObjectId(battery['user_id'])})

        battery["id"] = str(battery["_id"])
        battery["email"] = str(user["email"])
        battery["status"] = 'available'
        del battery["_id"]
        results.append(BatterySchema(**battery))

    return results

def service_battery_by_user_id(
    user_id: str,
):
    battery = db["battery"].find_one({"user_id": str(user_id)})
    battery["id"] = str(battery["_id"])
    del battery["_id"]

    # update battery saving
    get_all_season = db["pricing"].find()
    daylights = {}
    for season in get_all_season:
        daylights[season["season_name"]] = season["day_light"]
    current_date = datetime.now()
    created_at = battery["created_at"]
    periods = divide_into_periods(created_at, current_date)

    total_daylight_saving = 0
    for period in periods:
        print(period)
        season = period['season']
        start = period['start']
        end = period['end']
        num_days = (end - start).days + 1
        daylight = daylights.get(season, 0)  # Default to 0 if the season is not found
        print(num_days, daylight)
        total_daylight_saving += (num_days * daylight) * 50

    update_result = db["battery"].update_one(
        {
            "user_id": str(user_id),
        },
        {
            "$set": {
                "saved_energy": total_daylight_saving
            },
        },
        upsert=False,
    )
    # if update_result.modified_count == 0:
        # raise HTTPException(status_code=404, detail="battery not found")


    return BatterySchema(**battery)


def get_season(date):
    year = date.year
    seasons = {
        'winter': (datetime(year, 12, 21), datetime(year + 1, 3, 20)),
        'spring': (datetime(year, 3, 21), datetime(year, 6, 20)),
        'summer': (datetime(year, 6, 21), datetime(year, 9, 22)),
        'summer': (datetime(year, 9, 23), datetime(year, 12, 20)),
    }

    for season, (start, end) in seasons.items():
        if start <= date <= end:
            return season, start, end

    # Handle the case where the date is in the beginning of the year and belongs to last year's winter
    return 'Winter', datetime(year - 1, 12, 21), datetime(year, 3, 20)

def divide_into_periods(created_at, current_date):
    periods = []
    current = created_at

    while current <= current_date:
        season, start, end = get_season(current)
        period_end = min(end, current_date)
        periods.append({
            'season': season,
            'start': current,
            'end': period_end
        })
        current = period_end + timedelta(days=1)

    # Adjust the last period to end at the current date if it overshoots
    if periods and periods[-1]['end'] > current_date:
        periods[-1]['end'] = current_date

    return periods
















































































