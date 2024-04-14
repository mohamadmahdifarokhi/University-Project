from pymongo import MongoClient
from fastapi import HTTPException, status
from datetime import datetime
from .models import Order
from ..db.db import db
from ..logger import logger


class OrderService:
    def __init__(self):
        self.db = db

    def insert(self, req):
        """
        Insert a new order.

        Args:
            req: The order information to be inserted.

        Returns:
            dict: The inserted order.

        Raises:
            HTTPException: If the transaction ID already exists or internal server error occurs.
        """
        try:
            existing_order = self.db.orders.find_one({"transaction_id": req.transaction_id, "is_active": True})
            if existing_order:
                raise HTTPException(status_code=400, detail="Transaction id already exists")

            new_order = {
                "transaction_id": req.transaction_id,
                "user_id": req.user_id,
                "order_items": req.order_items,
                "created": datetime.utcnow(),
                "is_active": True
            }

            result = self.db.orders.insert_one(new_order)
            new_order["_id"] = str(result.inserted_id)

            logger.info(f"Inserted Order with ID: {new_order['_id']}")
            return new_order

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error inserting Order: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_by_user_id(self, user_id: str, page: int, page_size: int):
        
        try:

            offset = (page - 1) * page_size

            count = self.db.orders.count_documents({"user_id": user_id, "is_active": True})

            orders = self.db.orders.find({"user_id": user_id, "is_active": True}).sort("created", -1).skip(
                offset).limit(page_size)

            orders_list = list(orders)

            if not orders_list:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"message": "Orders not found", "code": 404},
                )

            # You can further process the orders here if needed

            return {"orders": orders_list, "count": count}

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error retrieving orders: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")