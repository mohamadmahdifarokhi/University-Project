import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OPTIONS_FILE = os.path.join(BASE_DIR, "prices.json")


def read_prices():
    with open(OPTIONS_FILE, "r") as file:
        options_data = json.load(file)
    return options_data


def write_prices(prices):
    with open(OPTIONS_FILE, "w") as file:
        json.dump(prices, file)
