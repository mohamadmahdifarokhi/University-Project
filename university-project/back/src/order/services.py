from pymongo import MongoClient
from fastapi import HTTPException, status
from datetime import datetime
from .models import Order
from ..logger import logger


class OrderService:
    def __init__(self, client: MongoClient, db_name: str):
        self.client = client
        self.db = self.client[db_name]

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
