import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from src.auth.models import Permission
from src.auth.routers import router as auth_router
from src.auth.schemas import VerifyOtpReq, OtpReq
from src.auth.services import UserService, OTPService
from src.cart.routers import router as cart_router
from src.category.admins import CategoryAdmin
from src.category.routers import router as category_router
from src.order.routers import router as order_router
from src.payment.routers import router as payment_router
from src.product.routers import router as product_router
from src.profile.routers import router as profile_router
from src.auth.admins import UserAdmin, OTPAdmin, TokenAdmin, PermissionAdmin, PermissionSetAdmin
from src.cart.admins import CartAdmin, CartItemAdmin
from src.order.admins import OrderAdmin, OrderItemAdmin
from src.product.admins import ProductAdmin
from src.profile.admins import ProfileAdmin
from src.core.admins import authentication_backend
from src.db.db import Base, engine, sess_db
from sqladmin import Admin
from .logger import logger

app = FastAPI(title="Uuniversity Project")

# Initialize SQL Admin
admin: Admin = Admin(app, engine, title="Uuniversity Project Service", authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(OTPAdmin)
admin.add_view(TokenAdmin)
admin.add_view(PermissionAdmin)
admin.add_view(PermissionSetAdmin)

admin.add_view(CartAdmin)
admin.add_view(CartItemAdmin)
admin.add_view(OrderAdmin)
admin.add_view(OrderItemAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(ProductAdmin)
admin.add_view(ProfileAdmin)

# Configure CORS
origins = [
    "http://localhost:3002",
    "http://accountract.com:3002",
    "http://accountract.com",
    "http://5.78.57.46:3002",
    "http://localhost:3001",
    "http://5.78.57.46:3001",
    "http://5.78.57.46:80",
    "http://5.78.57.46",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3002",
    "http://127.0.0.1:3001",
    "http://5.78.57.46:8000",
    "http://127.0.0.1:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables on startup
@app.get("/startup", tags=["Startup"])
async def on_startup():
    """
    Create tables on application startup.
    """
    Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(profile_router, prefix="/users/profiles")
app.include_router(category_router, prefix="/categories")
app.include_router(product_router, prefix="/products")
app.include_router(cart_router, prefix="/users/carts")
app.include_router(order_router, prefix="/users/orders")
app.include_router(payment_router, prefix="/users/payments")

Base.metadata.create_all(bind=engine)


def create_user_permission(sess: Session = next(sess_db())):
    """
    Create a 'user' permission in the database.
    """
    try:
        permission = Permission(name="user", description="user")
        sess.add(permission)
        sess.commit()

    except Exception as e:
        sess.rollback()
        logger.error(f"Error creating user permission: {e}")


def create_admin_permission(sess: Session = next(sess_db())):
    """
    Create an 'admin' permission in the database.
    """
    try:
        permission = Permission(name="admin", description="admin")
        sess.add(permission)
        sess.commit()

    except Exception as e:
        sess.rollback()
        logger.error(f"Error creating admin permission: {e}")


def create_admin(sess: Session = next(sess_db())):
    """
    Create an admin user in the database.
    """
    try:
        otp = OTPService(sess).insert(OtpReq(email="accountract@gmail.com"))
        UserService(sess).insert(
            req=VerifyOtpReq(email="accountract@gmail.com", password="accountract", otp_code=otp.otp_code),
            admin=True)
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")


# Execute database setup functions
create_user_permission()
create_admin_permission()
create_admin()

# Run the application using Uvicorn
if __name__ == '__main__':
    uvicorn.run('app:app', host="127.0.0.1", port=8010)
