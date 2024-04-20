from fastapi import FastAPI
from pymongo import MongoClient
from starlette.middleware.cors import CORSMiddleware

from src.auth.services import OTPService, UserService
from src.logger import logger
from src.order.routers import router as order_router
from src.profile.routers import router as profile_router
from src.auth.routers import router as auth_router
from src.device.api import router as device_router
from src.power_record.api import router as power_record_router
from src.pricing.api import router as pricing_router
from src.solar_panel.routers import router as solar_panel_router
import os
from dotenv import load_dotenv
from src.db import db
load_dotenv()

app = FastAPI(title="Uuniversity Project")
client = MongoClient(os.environ.get("DATABASE_URL"))
# Access your database
db = client["university"]
# Configure CORS
origins = [
    "http://localhost:80",
    "http://localhost:3000",
    "http://127.0.0.1:80",
    "http://127.0.0.1:3000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(profile_router, prefix="/users/profiles")
app.include_router(order_router, prefix="/users/orders")


app.include_router(device_router)
app.include_router(power_record_router)
app.include_router(pricing_router)
app.include_router(solar_panel_router)


# Create tables on startup
@app.get("/startup", tags=["Startup"])
async def on_startup():
    """
    Create collections on application startup.
    """
    # Define your MongoDB collections here
    db.create_collection('users')
    db.create_collection('permissions')
    db.create_collection('profiles')
    db.create_collection('carts')


# Define functions for creating permissions and admin user
def create_user_permission():
    """
    Create a 'user' permission in the database if it does not exist.
    """
    try:
        existing_permission = db.permissions.find_one({"name": "user"})
        if existing_permission is None:
            db.permissions.insert_one({"name": "user", "description": "user"})
    except Exception as e:
        logger.error(f"Error creating user permission: {e}")


def create_admin_permission():
    """
    Create an 'admin' permission in the database if it does not exist.
    """
    try:
        existing_permission = db.permissions.find_one({"name": "admin"})
        if existing_permission is None:
            db.permissions.insert_one({"name": "admin", "description": "admin"})
    except Exception as e:
        logger.error(f"Error creating admin permission: {e}")


def create_admin():
    """
    Create an admin user in the database.
    """
    try:
        otp = OTPService().insert({"email": "accountract@gmail.com"})
        print("asdasdsad")
        UserService().insert(req={
            "email": "accountract@gmail.com",
            "password": "accountract",
            "otp_code": otp['otp_code'],
        }, admin=True)
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")


# Execute database setup functions
create_user_permission()
create_admin_permission()
create_admin()

# Run the application using Uvicorn
if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app:app', host="127.0.0.1", port=8010)
