from bson import ObjectId
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.db import db
from .models import Order
from .schemas import *
from ..auth.models import User

from typing import Optional, List

from pymongo import MongoClient
from fastapi import HTTPException, status
from datetime import datetime
from .models import Order
from .schemas import OrderOut, OrderCreate, OrderUpdate
from ..db.db import db
from ..logger import logger
# from ..product.models import Product
from datetime import datetime

from pydantic_mongo import ObjectIdField
from bson import ObjectId


def service_create_order(
    order: OrderCreateSchema
):
    solar_panel = db["solar_panels"].find_one({"_id": ObjectId(order.solar_panel_id)})
    if solar_panel is None:
        raise HTTPException(status_code=404, detail="Solar panel not found.")

    if solar_panel["saved_capacity"] < order.amount:
        raise HTTPException(status_code=400, detail="Insufficient saved capacity.")
    
    seller_id = db["solar_panels"].find_one({"_id": ObjectId(order.solar_panel_id)})["user_id"]
    base_order = OrderCreateSchema(
        user_id=order.user_id,
        solar_panel_id=order.solar_panel_id,
        seller_id=seller_id,
        amount=order.amount,
        fee=order.amount*50,
        created_at=str(datetime.now())
    ).model_dump()
    db["orders"].insert_one(base_order)
    update_result = db["solar_panels"].update_one(
        {
            "_id": ObjectId(order.solar_panel_id),
        },
        {
            "$set": {
                "saved_capacity": solar_panel["saved_capacity"] - order.amount,
                "sold_capacity": solar_panel["sold_capacity"] + order.amount,
            },
        },
        upsert=False,
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Solar panel not found")
    return {"detail": "order added"}
    
def service_get_order_all(
):
    orders = db["orders"].find()
    results = []
    for order in orders:
        order["id"] = str(order["_id"])
        del order["_id"]
        results.append(OrderCreateSchema(**order))

    return results


def service_get_order_buy_user(
    user_id: str,
):
    orders = db["orders"].find({"user_id": str(user_id)})
    results = []
    for order in orders:
        order["id"] = str(order["_id"])
        order["created_at"] = order["created_at"].strftime("%d-%b-%Y")
        del order["_id"]
        results.append(OrderOutputSchema(**order))
    return results

def service_get_order_sell_user(
    user_id: str,
):
    orders = db["orders"].find({"seller_id": str(user_id)})
    results = []
    for order in orders:
        order["id"] = str(order["_id"])
        order["created_at"] = order["created_at"].strftime("%d-%b-%Y")
        del order["_id"]
        results.append(OrderOutputSchema(**order))
    return results

def service_delete_order(
    order_id: str,
):
    update_result = db["orders"].delete_one(
        {"_id": ObjectId(order_id)},
    )
    return {"detail": "order deleted."}


def service_last_orders(
        db
):
    orders = db["orders"].find().sort({"created_at": -1}).limit(5)
    results = []
    for order in orders:
        order["id"] = str(order["_id"])
        del order["_id"]
        results.append(OrderCreateSchema(**order))
    return results


# class OrderService:
#     def __init__(self, sess: Session):
#         self.sess: Session = sess

#     def insert(self, req: OrderReq) -> Order:

# class OrderService:
#     def __init__(self, sess: Session):
#         self.sess: Session = sess

#     def insert(self, req: OrderReq) -> Order:
#         """
#         Insert a new order.

#         Args:
#             req: The order information to be inserted.

#         Returns:
#             Order: The inserted order.

#         Raises:
#             HTTPException: If the transaction ID already exists or internal server error occurs.
#         """
#         try:
#             existing_order = (self.sess.query(Order).filter_by(transaction_id=req.transaction_id, is_active=True)
#                               .first())
#             if existing_order:
#                 raise HTTPException(status_code=400, detail="Transaction id already exists")

#             new_order = Order(**req.__dict__)
#             self.sess.add(new_order)
#             self.sess.commit()

#             logger.info(f"Inserted Order with ID: {new_order.id}")
#             return new_order

#         except HTTPException:
#             raise

#         except Exception as e:
#             self.sess.rollback()
#             logger.error(f"Error inserting Order: {str(e)}")
#             raise HTTPException(status_code=500, detail="Internal server error")

#     def get_order_by_id(self, orderId: UUID):
#         """Retrieve an order by its ID along with associated order items."""
#         order = self.sess.query(Order).filter_by(id=orderId).first()
#         if not order:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=Error(
#                     message="Order not found",
#                     code=404,
#                 ).dict(),
#             )
# class OrderService:
#     def __init__(self):
#         self.db = db

#     def insert(self, req):
#         """
#         Insert a new order.

#         Args:
#             req: The order information to be inserted.

#         Returns:
#             Order: The inserted order.
#             dict: The inserted order.

#         Raises:
#             HTTPException: If the transaction ID already exists or internal server error occurs.
#         """
#         try:
#             existing_order = (self.sess.query(Order).filter_by(transaction_id=req.transaction_id, is_active=True)
#                               .first())
#             if existing_order:
#                 raise HTTPException(status_code=400, detail="Transaction id already exists")

#             new_order = Order(**req.__dict__)
#             self.sess.add(new_order)
#             self.sess.commit()

#             logger.info(f"Inserted Order with ID: {new_order.id}")
#             return new_order

#         except HTTPException:
#             raise

#         except Exception as e:
#             self.sess.rollback()
#             logger.error(f"Error inserting Order: {str(e)}")
#             raise HTTPException(status_code=500, detail="Internal server error")

#     def get_order_by_id(self, orderId: UUID):
#         """Retrieve an order by its ID along with associated order items."""
#         order = self.sess.query(Order).filter_by(id=orderId).first()
#         if not order:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=Error(
#                     message="Order not found",
#                     code=404,
#                 ).dict(),
#             )
    
#         order_items = self.sess.query(OrderItem).filter_by(orderId=orderId).all()
#         order.orderItem = order_items
#         print("-------")
#         print(type(order))
#         # print(order)
#         print(order.__dict__)
#         print("-------")
#         return order

#     def get_by_user_id(self, user: User, page: int, page_size: int):
#         """
#         Retrieve orders by user ID along with associated order items and products with pagination.

#         Args:
#             user: The user for whom to retrieve orders.
#             page: The page number for pagination.
#             page_size: Number of orders per page.

#         Returns:
#             dict: A dictionary containing a list of orders and the total count.

#         Raises:
#             HTTPException: If orders are not found or internal server error occurs.
#         """
#         try:
#             offset = (page - 1) * page_size
#             count = self.sess.query(Order).filter_by(user_id=user.id, is_active=True).count()
#             orders = self.sess.query(Order).filter_by(user_id=user.id, is_active=True).order_by(
#                 Order.created.desc()).offset(offset).limit(page_size).all()

#             if not orders:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND,
#                     detail={"message": "Orders not found", "code": 404},
#                 )
#             prices = read_prices()
#             for order in orders:
#                 for order_item in order.order_items:
#                     order_item.price = float(prices["usd"]["value"]) * float(order_item.price)
#             return {"orders": orders, "count": count}

#         except HTTPException:
#             raise

#         except Exception as e:
#             logger.error(f"Error retrieving orders: {str(e)}")
#             raise HTTPException(status_code=500, detail="Internal server error")

#     def update_order(self, orderId: UUID, order_input: OrderUpdate):
#         """Update an order with patch update."""
#         order = self.get_order_by_id(orderId)
    
#         if order:
#             for field, value in order_input.dict(exclude_unset=True).items():
#                 setattr(order, field, value)
    
#             self.sess.commit()
#             self.sess.refresh(order)
    
#         return order

#     def delete_order(self, orderId: UUID):
#         """Delete an order by its ID."""
#         order = self.get_order_by_id(orderId)
#         if order:
#             self.sess.delete(order)
#             self.sess.commit()



#   def get_orderItem_by_id(self, orderItem_id: UUID):
#         """Retrieve an order item by its ID."""

#         orderItem = self.sess.query(OrderItem).filter_by(id=orderItem_id).first()
#         if not orderItem:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=Error(
#                     message="Order not found",
#                     code=404,
#                 ).dict(),
#             )
#         return orderItem

#     def update_orderItem(self, orderItem_id: UUID, orderItem_input: OrderItemUpdate):
#         """Update an order item with patch update."""
#         orderItem = self.get_orderItem_by_id(orderItem_id)

#         if orderItem:
#             for field, value in orderItem_input.dict(exclude_unset=True).items():
#                 setattr(orderItem, field, value)

#             self.sess.commit()
#             self.sess.refresh(orderItem)

#         return orderItem

#     def delete_orderItem(self, orderItem_id: UUID):
#         """Delete an order item by its ID."""
#         orderItem = self.get_orderItem_by_id(orderItem_id)
#         if orderItem:
#             self.sess.delete(orderItem)
#             self.sess.commit()
#         return order

#     def delete_order(self, orderId: UUID):
#         """Delete an order by its ID."""
#         order = self.get_order_by_id(orderId)
#         if order:
#             self.sess.delete(order)
#             self.sess.commit()



#   def get_orderItem_by_id(self, orderItem_id: UUID):
#         """Retrieve an order item by its ID."""

#         orderItem = self.sess.query(OrderItem).filter_by(id=orderItem_id).first()
#         if not orderItem:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=Error(
#                     message="Order not found",
#                     code=404,
#                 ).dict(),
#             )
#         return orderItem

#     def update_orderItem(self, orderItem_id: UUID, orderItem_input: OrderItemUpdate):
#         """Update an order item with patch update."""
#         orderItem = self.get_orderItem_by_id(orderItem_id)

#         if orderItem:
#             for field, value in orderItem_input.dict(exclude_unset=True).items():
#                 setattr(orderItem, field, value)

#             self.sess.commit()
#             self.sess.refresh(orderItem)

#         return orderItem

#     def delete_orderItem(self, orderItem_id: UUID):
#         """Delete an order item by its ID."""
#         orderItem = self.get_orderItem_by_id(orderItem_id)
#         if orderItem:
#             self.sess.delete(orderItem)
#             self.sess.commit()
#             existing_order = self.db.orders.find_one({"transaction_id": req.transaction_id, "is_active": True})
#             if existing_order:
#                 raise HTTPException(status_code=400, detail="Transaction id already exists")

#             new_order = {
#                 "transaction_id": req.transaction_id,
#                 "user_id": req.user_id,
#                 "order_items": req.order_items,
#                 "created": datetime.utcnow(),
#                 "is_active": True
#             }

#             result = self.db.orders.insert_one(new_order)
#             new_order["_id"] = str(result.inserted_id)

#             logger.info(f"Inserted Order with ID: {new_order['_id']}")
#             return new_order


#         except HTTPException:
#             raise


#         except Exception as e:
#             self.sess.rollback()
#             logger.error(f"Error inserting Order: {str(e)}")
#             raise HTTPException(status_code=500, detail="Internal server error")

    # def get_order_by_id(self, orderId: UUID):
    #     """Retrieve an order by its ID along with associated order items."""
    #     order = self.sess.query(Order).filter_by(id=orderId).first()
    #     if not order:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=Error(
    #                 message="Order not found",
    #                 code=404,
    #             ).dict(),
    #         )
    #
    #     order_items = self.sess.query(OrderItem).filter_by(orderId=orderId).all()
    #     order.orderItem = order_items
    #     print("-------")
    #     print(type(order))
    #     # print(order)
    #     print(order.__dict__)
    #     print("-------")
    #     return order

    # def get_by_user_id(self, user: User, page: int, page_size: int):
    #     """
    #     Retrieve orders by user ID along with associated order items and products with pagination.

    #     Args:
    #         user: The user for whom to retrieve orders.
    #         page: The page number for pagination.
    #         page_size: Number of orders per page.

    #     Returns:
    #         dict: A dictionary containing a list of orders and the total count.

    #     Raises:
    #         HTTPException: If orders are not found or internal server error occurs.
    #     """
    #     try:
    #         offset = (page - 1) * page_size
    #         count = self.sess.query(Order).filter_by(user_id=user.id, is_active=True).count()
    #         orders = self.sess.query(Order).filter_by(user_id=user.id, is_active=True).order_by(
    #             Order.created.desc()).offset(offset).limit(page_size).all()

    #         if not orders:
    #             raise HTTPException(
    #                 status_code=status.HTTP_404_NOT_FOUND,
    #                 detail={"message": "Orders not found", "code": 404},
    #             )
    #         prices = read_prices()
    #         for order in orders:
    #             for order_item in order.order_items:
    #                 order_item.price = float(prices["usd"]["value"]) * float(order_item.price)
    #         return {"orders": orders, "count": count}

    #     except HTTPException:
    #         raise

    #     except Exception as e:
    #         logger.error(f"Error retrieving orders: {str(e)}")
    #         raise HTTPException(status_code=500, detail="Internal server error")

    # def update_order(self, orderId: UUID, order_input: OrderUpdate):
    #     """Update an order with patch update."""
    #     order = self.get_order_by_id(orderId)
    #
    #     if order:
    #         for field, value in order_input.dict(exclude_unset=True).items():
    #             setattr(order, field, value)
    #
    #         self.sess.commit()
    #         self.sess.refresh(order)
    #
    #     return order

    # def delete_order(self, orderId: UUID):
    #     """Delete an order by its ID."""
    #     order = self.get_order_by_id(orderId)
    #     if order:
    #         self.sess.delete(order)
    #         self.sess.commit()


#
#   def get_orderItem_by_id(self, orderItem_id: UUID):
#         """Retrieve an order item by its ID."""
#
#         orderItem = self.sess.query(OrderItem).filter_by(id=orderItem_id).first()
#         if not orderItem:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=Error(
#                     message="Order not found",
#                     code=404,
#                 ).dict(),
#             )
#         return orderItem
#
#     def update_orderItem(self, orderItem_id: UUID, orderItem_input: OrderItemUpdate):
#         """Update an order item with patch update."""
#         orderItem = self.get_orderItem_by_id(orderItem_id)
#
#         if orderItem:
#             for field, value in orderItem_input.dict(exclude_unset=True).items():
#                 setattr(orderItem, field, value)
#
#             self.sess.commit()
#             self.sess.refresh(orderItem)
#
#         return orderItem
#
#     def delete_orderItem(self, orderItem_id: UUID):
#         """Delete an order item by its ID."""
#         orderItem = self.get_orderItem_by_id(orderItem_id)
#         if orderItem:
#             self.sess.delete(orderItem)
#             self.sess.commit()

    #     except Exception as e:
    #         logger.error(f"Error inserting Order: {str(e)}")
    #         raise HTTPException(status_code=500, detail="Internal server error")
    #
    # def get_by_user_id(self, user_id: str, page: int, page_size: int):
    #
    #     try:
    #
    #         offset = (page - 1) * page_size
    #
    #         count = self.db.orders.count_documents({"user_id": user_id, "is_active": True})
    #
    #         orders = self.db.orders.find({"user_id": user_id, "is_active": True}).sort("created", -1).skip(
    #             offset).limit(page_size)
    #
    #         orders_list = list(orders)
    #
    #         if not orders_list:
    #             raise HTTPException(
    #                 status_code=status.HTTP_404_NOT_FOUND,
    #                 detail={"message": "Orders not found", "code": 404},
    #             )
    #
    #         # You can further process the orders here if needed
    #
    #         return {"orders": orders_list, "count": count}
    #
    #     except HTTPException:
    #         raise
    #
    #     except Exception as e:
    #         logger.error(f"Error retrieving orders: {str(e)}")
    #         raise HTTPException(status_code=500, detail="Internal server error")
    #
    # def create_order(self, order_data: OrderCreate) -> OrderOut:
    #     order_id = ObjectId()
    #     order_data_dict = order_data.dict()
    #     order_data_dict["_id"] = order_id
    #     self.db.orders.insert_one(order_data_dict)
    #     return OrderOut(id=str(order_id), **order_data_dict)
    #
    # def get_orders(self, skip: int = 0, limit: int = 10) -> List[OrderOut]:
    #     orders = list(self.db.orders.find().skip(skip).limit(limit))
    #     for order in orders:
    #         order["_id"] = str(order["_id"])
    #     return orders
    #
    # def get_order(self, order_id: str) -> Optional[OrderOut]:
    #     order = self.db.orders.find_one({"_id": ObjectId(order_id)})
    #     if order:
    #         order["_id"] = str(order["_id"])
    #         return order
    #     return None
    #
    # def update_order(self, order_id: str, order_update: OrderUpdate) -> Optional[OrderOut]:
    #     update_data = order_update.dict(exclude_unset=True)
    #     result = self.db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": update_data})
    #     if result.modified_count:
    #         updated_order = self.db.orders.find_one({"_id": ObjectId(order_id)})
    #         updated_order["_id"] = str(updated_order["_id"])
    #         return updated_order
    #     return None
    #
    # def delete_order(self, order_id: str) -> Optional[OrderOut]:
    #     order = self.db.orders.find_one({"_id": ObjectId(order_id)})
    #     if order:
    #         self.db.orders.delete_one({"_id": ObjectId(order_id)})
    #         order["_id"] = str(order["_id"])
    #         return order
    #     return None
