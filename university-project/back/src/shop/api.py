from fastapi import APIRouter, Depends, Body, Response, status

from src.auth.models import User
from src.auth.secures import get_current_user
from .services import (
    service_list_categories,
    service_list_products,
    service_get_product_by_slug,
    service_get_cart,
    service_add_cart_item,
    service_remove_cart_item,
)

# Products & categories (public)
catalog_router = APIRouter(tags=["Shop"])


@catalog_router.get("/categories", summary="Get all categories")
def list_categories():
    return service_list_categories()


@catalog_router.get("/products/", summary="Get active products")
def list_products(page: int = 1, page_size: int = 10):
    return service_list_products(is_active=True, page=page, page_size=page_size)


@catalog_router.get("/products/isActivate/false/", summary="Get not active products")
def list_not_active_products(page: int = 1, page_size: int = 10):
    return service_list_products(is_active=False, page=page, page_size=page_size)


@catalog_router.get("/products/{slug}", summary="Get a product by slug")
def get_product(slug: str):
    product = service_get_product_by_slug(slug)
    if not product:
        return {"detail": "Product not found"}
    return product


# Cart (authenticated) — mounted under /users/carts
cart_router = APIRouter(tags=["Cart"])


@cart_router.get("", summary="Get current user's cart")
@cart_router.get("/", summary="Get current user's cart")
def get_cart(user: User = Depends(get_current_user)):
    return service_get_cart(user["_id"])


@cart_router.post("/items", summary="Add an item to the cart")
def add_cart_item(
    payload: dict = Body(...),
    user: User = Depends(get_current_user),
):
    product_id = payload.get("product_id")
    count = payload.get("count", 1)
    if not product_id:
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return service_add_cart_item(user["_id"], product_id, count)


@cart_router.delete("/items/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove an item from the cart")
def remove_cart_item(
    product_id: str,
    user: User = Depends(get_current_user),
):
    service_remove_cart_item(user["_id"], product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
