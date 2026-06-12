import os
from dotenv import load_dotenv
from pymongo import MongoClient
from src.logger import logger
load_dotenv()
client = MongoClient(os.environ.get("DATABASE_URL"))
# Access your database
db = client["university"]
# Access your collection
