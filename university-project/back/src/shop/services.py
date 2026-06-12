from bson import ObjectId

from ..db.db import db


def _serialize_category(category):
    return {
        "id": str(category["_id"]),
        "name": category.get("name", {}),
    }


def _serialize_product(product):
    category = None
    if product.get("category_id"):
        cat = db["categories"].find_one({"_id": ObjectId(product["category_id"])})
        if cat:
            category = _serialize_category(cat)
    return {
        "id": str(product["_id"]),
        "slug": product.get("slug"),
        "name": product.get("name", {}),
        "description": product.get("description", {}),
        "price": product.get("price", 0),
        "logo": product.get("logo"),
        "photo": product.get("photo"),
        "background": product.get("background"),
        "isActivate": product.get("isActivate", True),
        "category": category,
    }


def service_list_categories():
    return [_serialize_category(c) for c in db["categories"].find()]


def service_list_products(is_active=True, page=1, page_size=10):
    skip = (page - 1) * page_size
    cursor = (
        db["products"]
        .find({"isActivate": is_active})
        .skip(skip)
        .limit(page_size)
    )
    return [_serialize_product(p) for p in cursor]


def service_get_product_by_slug(slug):
    product = db["products"].find_one({"slug": slug})
    if not product:
        return None
    return _serialize_product(product)


def _empty_cart(user_id):
    return {"user_id": str(user_id), "cart_items": []}


def service_get_cart(user_id):
    cart = db["carts"].find_one({"user_id": str(user_id)})
    if not cart:
        return _empty_cart(user_id)

    items = []
    for item in cart.get("cart_items", []):
        product = None
        if item.get("product_id"):
            prod = db["products"].find_one({"_id": ObjectId(item["product_id"])})
            if prod:
                product = _serialize_product(prod)
        items.append({"product": product, "count": item.get("count", 1)})
    return {"cart_items": items}


def service_add_cart_item(user_id, product_id, count=1):
    cart = db["carts"].find_one({"user_id": str(user_id)})
    if not cart:
        db["carts"].insert_one(
            {"user_id": str(user_id), "cart_items": [{"product_id": product_id, "count": count}]}
        )
        return service_get_cart(user_id)

    items = cart.get("cart_items", [])
    for item in items:
        if item.get("product_id") == product_id:
            item["count"] = item.get("count", 1) + count
            break
    else:
        items.append({"product_id": product_id, "count": count})

    db["carts"].update_one({"user_id": str(user_id)}, {"$set": {"cart_items": items}})
    return service_get_cart(user_id)
