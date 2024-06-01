import math
from ..db.db import client, db
from fastapi import Depends, HTTPException
import pymongo
from datetime import datetime
from bson import ObjectId
from .schemas import *
from fastapi.responses import JSONResponse
from src.auth.models import User
from src.auth.secures import get_current_user


def service_show_records_on_chart_super_admin(user_id, date=None):  
    if date is None:
        date = datetime.now().date()
    else:
        date = datetime.strptime(date, '%Y-%m-%d').date()

    start_time = datetime.combine(date, datetime.min.time())
    end_time = datetime.combine(date, datetime.max.time())

    # Aggregation pipeline to sum up consumption for each device
    pipeline = [
        {
            "$match": {
                # "user_id": ObjectId(str(user_id)),
                "start_time": {"$gte": start_time, "$lt": end_time}
            }
        },
        {
            "$group": {
                "_id": "$device_name",  # Group by device name
                "total_consumption": {"$sum": "$consumption"}  # Sum up consumption
            }
        },
        {
            "$project": {
                "_id": 0,
                "device_name": "$_id",
                "total_consumption": 1
            }
        }
    ]

    results = db["power_records"].aggregate(pipeline)
    result_dict = {doc["device_name"]: doc["total_consumption"] for doc in results}
    res = {
        "categories": list(result_dict.keys()),
        "values": list(result_dict.values())
    }

    return res


def service_show_records_on_chart_monthly_super_admin(user_id, year, month):
    year = int(year)
    month = int(month)
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)

    pipeline = [
        {
            '$match': {
                # 'user_id': ObjectId(str(user_id)),
                'start_time': {'$gte': start_date},
                'end_time': {'$lt': end_date}
            }
        },
        {
            '$group': {
                '_id': {
                    'device_name': '$device_name',
                    'day': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$start_time'}}
                },
                'total_consumption': {'$sum': '$consumption'}
            }
        },
        {
            '$project': {
                '_id': 0,
                'device_name': '$_id.device_name',
                'date': '$_id.day',
                'total_consumption': 1
            }
        },
        {
            '$sort': {
                'device_name': 1,
                'date': 1
            }
        }
    ]

    results = list(db["power_records"].aggregate(pipeline))
    categories = sorted({record['date'] for record in results})
    device_data = {}

    for record in results:
        device_name = record['device_name']
        if device_name not in device_data:
            device_data[device_name] = {date: 0 for date in categories}
        device_data[device_name][record['date']] = record['total_consumption']

    formatted_output = [
        {
            'name': device_name,
            'data': [device_data[device_name][date] for date in categories]
        }
        for device_name in sorted(device_data)
    ]

    return formatted_output, categories



def get_season_dates(season, year):
    if season == "Winter":
        start_date = datetime(year, 12, 21)
        end_date = datetime(year + 1, 3, 20)
    elif season == "Spring":
        start_date = datetime(year, 3, 21)
        end_date = datetime(year, 6, 20)
    elif season == "Summer":
        start_date = datetime(year, 6, 21)
        end_date = datetime(year, 9, 22)
    elif season == "Fall":
        start_date = datetime(year, 9, 23)
        end_date = datetime(year, 12, 20)
    else:
        raise ValueError("Invalid season name")
    return start_date, end_date


def service_show_seasonal_records_on_chart_super_admin(user_id, season, year):
    start_date, end_date = get_season_dates(season, year)

    pipeline = [
        {
            '$match': {
                # 'user_id': ObjectId(user_id),
                'start_time': {  # Assuming your field is `start_time`
                    '$gte': start_date,
                    '$lt': end_date
                }
            }
        },
        {
            '$group': {
                '_id': '$device_name',
                'total_usage': {'$sum': '$consumption'}
            }
        }
    ]

    try:
        result = list(db["power_records"].aggregate(pipeline))
        return result
    except Exception as e:
        print("An error occurred:", e)
        return []


def get_current_season():
    now = datetime.now()
    month = now.month
    day = now.day

    if (month == 3 and day >= 20) or month in [4, 5] or (month == 6 and day < 21):
        return "spring"
    elif (month == 6 and day >= 21) or month in [7, 8] or (month == 9 and day < 23):
        return "summer"
    elif (month == 9 and day >= 23) or month in [10, 11] or (month == 12 and day < 21):
        return "fall"
    else:
        return "winter"


def get_season(date):
    month = date.month
    if 3 <= month <= 5:
        return "spring"
    elif 6 <= month <= 8:
        return "summer"
    elif 9 <= month <= 11:
        return "summer"
    else:
        return "winter"


def service_cal_graph4_super_admin(
        user_id

):
    block = db["blocks"].find_one({"user_id": str(user_id)})
    if block:
        pipeline = [
            {

                "$addFields": {
                    "season": {
                        "$switch": {
                            "branches": [
                                {
                                    "case": {
                                        "$or": [
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 12]},
                                                      {"$gte": [{"$dayOfMonth": "$start_time"}, 21]}]},
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 1]},
                                                      {"$lte": [{"$dayOfMonth": "$start_time"}, 31]}]},
                                            {"$eq": [{"$month": "$start_time"}, 2]},
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 3]},
                                                      {"$lte": [{"$dayOfMonth": "$start_time"}, 20]}]}
                                        ]
                                    },
                                    "then": "winter"
                                },
                                {
                                    "case": {
                                        "$or": [
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 3]},
                                                      {"$gte": [{"$dayOfMonth": "$start_time"}, 21]}]},
                                            {"$eq": [{"$month": "$start_time"}, 4]},
                                            {"$eq": [{"$month": "$start_time"}, 5]},
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 6]},
                                                      {"$lte": [{"$dayOfMonth": "$start_time"}, 20]}]}
                                        ]
                                    },
                                    "then": "spring"
                                },
                                {
                                    "case": {
                                        "$or": [
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 6]},
                                                      {"$gte": [{"$dayOfMonth": "$start_time"}, 21]}]},
                                            {"$eq": [{"$month": "$start_time"}, 7]},
                                            {"$eq": [{"$month": "$start_time"}, 8]},
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 9]},
                                                      {"$lte": [{"$dayOfMonth": "$start_time"}, 20]}]}
                                        ]
                                    },
                                    "then": "summer"
                                },
                                {
                                    "case": {
                                        "$or": [
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 9]},
                                                      {"$gte": [{"$dayOfMonth": "$start_time"}, 21]}]},
                                            {"$eq": [{"$month": "$start_time"}, 10]},
                                            {"$eq": [{"$month": "$start_time"}, 11]},
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 12]},
                                                      {"$lte": [{"$dayOfMonth": "$start_time"}, 20]}]}
                                        ]
                                    },
                                    "then": "fall"
                                }
                            ],
                            "default": "Unknown"
                        }
                    }
                }
            },
            {
                "$group": {
                    "_id": "$season",
                    "totalConsumption": {
                        "$sum": "$consumption"
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "season": "$_id",
                    "totalConsumption": 1
                }
            }
        ]
        dc_coefficient = {
            "spring": {
                80: 126.6,
                100: 134.2,
                120: 135
            },
            "summer": {
                80: 133,
                100: 141,
                120: 142.5
            },
            "fall": {
                80: 97,
                100: 102,
                120: 103.4
            },
            "winter": {
                80: 78,
                100: 82,
                120: 83.2
            }
        }
        season = get_current_season()
        unoptimized_seasons = list(db["power_records"].aggregate(pipeline))
        seasons_pv_gen = []
        unoptimized_seasonss = []
        for optimized_season in unoptimized_seasons:
            pv_gen = (((int(block['area']) * 0.75) / 1.65) * dc_coefficient[optimized_season["season"]][
                int(block['area'])]) * 90
            seasons_pv_gen.append({'season': optimized_season["season"], 'pv_gen': pv_gen})
            unoptimized = (abs(pv_gen - optimized_season['totalConsumption']) * 0.95 / 1000)
            unoptimized_seasonss.append({'season': optimized_season["season"], 'unoptimized': unoptimized})

        pipeline = [
            {

                "$addFields": {
                    "season": {
                        "$switch": {
                            "branches": [
                                {
                                    "case": {
                                        "$or": [
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 12]},
                                                      {"$gte": [{"$dayOfMonth": "$start_time"}, 21]}]},
                                            {"$eq": [{"$month": "$start_time"}, 1]},
                                            {"$eq": [{"$month": "$start_time"}, 2]},
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 3]},
                                                      {"$lte": [{"$dayOfMonth": "$start_time"}, 20]}]}
                                        ]
                                    },
                                    "then": "winter"
                                },
                                {
                                    "case": {
                                        "$or": [
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 3]},
                                                      {"$gte": [{"$dayOfMonth": "$start_time"}, 21]}]},
                                            {"$eq": [{"$month": "$start_time"}, 4]},
                                            {"$eq": [{"$month": "$start_time"}, 5]},
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 6]},
                                                      {"$lte": [{"$dayOfMonth": "$start_time"}, 20]}]}
                                        ]
                                    },
                                    "then": "spring"
                                },
                                {
                                    "case": {
                                        "$or": [
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 6]},
                                                      {"$gte": [{"$dayOfMonth": "$start_time"}, 21]}]},
                                            {"$eq": [{"$month": "$start_time"}, 7]},
                                            {"$eq": [{"$month": "$start_time"}, 8]},
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 9]},
                                                      {"$lte": [{"$dayOfMonth": "$start_time"}, 20]}]}
                                        ]
                                    },
                                    "then": "summer"
                                },
                                {
                                    "case": {
                                        "$or": [
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 9]},
                                                      {"$gte": [{"$dayOfMonth": "$start_time"}, 21]}]},
                                            {"$eq": [{"$month": "$start_time"}, 10]},
                                            {"$eq": [{"$month": "$start_time"}, 11]},
                                            {"$and": [{"$eq": [{"$month": "$start_time"}, 12]},
                                                      {"$lte": [{"$dayOfMonth": "$start_time"}, 20]}]}
                                        ]
                                    },
                                    "then": "fall"
                                }
                            ],
                            "default": "Unknown"
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "adjustedConsumption": {
                        "$cond": {
                            "if": {
                                "$or": [
                                    {"$eq": ["$device", "air conditioner(small)"]},
                                    {"$eq": ["$device", "air conditioner(medium)"]},
                                    {"$eq": ["$device", "air conditioner(large)"]},
                                    {"$eq": ["$device", "heater (small)"]},
                                    {"$eq": ["$device", "heater (medium)"]},
                                    {"$eq": ["$device", "heater (large)"]},
                                ]
                            },
                            "then": {"$multiply": ["$consumption", 0.33]},
                            "else": "$consumption"
                        }
                    }
                }
            },
            {
                "$group": {
                    "_id": "$season",
                    "totalConsumption": {
                        "$sum": "$adjustedConsumption"
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "season": "$_id",
                    "totalConsumption": 1
                }
            }
        ]

        optimized_seasons = list(db["power_records"].aggregate(pipeline))
        season = get_current_season()
        seasons_pv_gen = []
        optimized_seasonss = []
        for optimized_season in optimized_seasons:
            pv_gen = (((int(block['area']) * 0.75) / 1.65) * dc_coefficient[optimized_season["season"]][
                int(block['area'])]) * 90
            seasons_pv_gen.append({'season': optimized_season["season"], 'pv_gen': pv_gen})
            optimized = (abs(pv_gen - optimized_season['totalConsumption']) * 0.55 / 1000)
            optimized_seasonss.append({'season': optimized_season["season"], 'optimized': optimized})
        seasons_order = ["spring", "summer", "fall", "winter"]
        unoptimized_seasonss = sorted(unoptimized_seasonss, key=lambda x: seasons_order.index(x['season']))
        optimized_seasonss = sorted(optimized_seasonss, key=lambda x: seasons_order.index(x['season']))
        un = [int(uno['unoptimized']) for uno in unoptimized_seasonss]
        op = [int(uno['optimized']) for uno in optimized_seasonss]
        return un, op
    else:
        return 0, 0



def service_get_all_user(
    user_id
):
    users = db["users"].find({})

    for user in users:
        user["id"] = str(user["_id"])
        del user["_id"]
        return user





































































