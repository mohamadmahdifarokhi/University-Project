from fastapi import FastAPI
from pymongo.errors import CollectionInvalid
from starlette.middleware.cors import CORSMiddleware

from src.auth.secures import get_password_hash
from src.logger import logger
from src.battery.api import router as battery_router
from src.profile.routers import router as profile_router
from src.auth.routers import router as auth_router
from src.device.api import router as device_router
from src.block.api import router as block_router
from src.apartment.api import router as apartment_router
from src.power_record.api import router as power_record_router
from src.pricing.api import router as pricing_router
from src.solar_panel.routers import router as solar_panel_router
from src.admins.api import router as admin_router
from dotenv import load_dotenv
from src.db.db import db
load_dotenv()

app = FastAPI(title="دانشگاه آزاد اسلامی واحد پردیس")
# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:80",
    "http://127.0.0.1:3000",
    "http://188.34.155.23",
    "http://188.34.155.23:3000",
    "http://188.34.155.23:80"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(profile_router, prefix="/users/profiles")


app.include_router(apartment_router)
app.include_router(block_router)
app.include_router(battery_router)
app.include_router(device_router)
app.include_router(power_record_router)
app.include_router(pricing_router)
app.include_router(solar_panel_router)
app.include_router(admin_router)


# Create tables on startup
@app.get("/startup", tags=["Startup"])
async def on_startup():
    """
    Create collections on application startup.
    """
    for collection_name in ("users", "permissions", "profiles"):
        try:
            db.create_collection(collection_name)
        except CollectionInvalid:
            pass


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
        if db.users.find_one({"email": "admin@gmail.com"}):
            return
        permissions = [p for p in db.permissions.find({"name": {"$in": ["user", "admin"]}})]
        db.users.insert_one({
            "email": "admin@gmail.com",
            "password": get_password_hash("admin"),
            "provider": "local",
            "permissions": permissions,
        })
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
