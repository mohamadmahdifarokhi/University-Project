from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Order, OrderItem
from .schemas import OrderReq, OrderItemReq
from ..auth.models import User
from ..logger import logger
from ..payment.utils import read_prices
from ..product.models import Product


class OrderService:
    def __init__(self, sess: Session):
        self.sess: Session = sess

    def insert(self, req: OrderReq) -> Order:
        """
        Insert a new order.

        Args:
            req: The order information to be inserted.

        Returns:
            Order: The inserted order.

        Raises:
            HTTPException: If the transaction ID already exists or internal server error occurs.
        """
        try:
            existing_order = (self.sess.query(Order).filter_by(transaction_id=req.transaction_id, is_active=True)
                              .first())
            if existing_order:
                raise HTTPException(status_code=400, detail="Transaction id already exists")

            new_order = Order(**req.__dict__)
            self.sess.add(new_order)
            self.sess.commit()

            logger.info(f"Inserted Order with ID: {new_order.id}")
            return new_order

        except HTTPException:
            raise

        except Exception as e:
            self.sess.rollback()
            logger.error(f"Error inserting Order: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

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

    def get_by_user_id(self, user: User, page: int, page_size: int):
        """
        Retrieve orders by user ID along with associated order items and products with pagination.

        Args:
            user: The user for whom to retrieve orders.
            page: The page number for pagination.
            page_size: Number of orders per page.

        Returns:
            dict: A dictionary containing a list of orders and the total count.

        Raises:
            HTTPException: If orders are not found or internal server error occurs.
        """
        try:
            offset = (page - 1) * page_size
            count = self.sess.query(Order).filter_by(user_id=user.id, is_active=True).count()
            orders = self.sess.query(Order).filter_by(user_id=user.id, is_active=True).order_by(
                Order.created.desc()).offset(offset).limit(page_size).all()

            if not orders:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"message": "Orders not found", "code": 404},
                )
            prices = read_prices()
            for order in orders:
                for order_item in order.order_items:
                    order_item.price = float(prices["usd"]["value"]) * float(order_item.price)
            return {"orders": orders, "count": count}

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error retrieving orders: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

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


class order_itemservice:
    def __init__(self, sess: Session):
        self.sess: Session = sess

    def insert(self, req: OrderItemReq) -> OrderItem:
        """
        Insert a new order item.

        Args:
            req: The order item information to be inserted.

        Returns:
            OrderItem: The inserted order item.

        Raises:
            HTTPException: If the product or order is not found or internal server error occurs.
        """
        try:
            product = self.sess.query(Product).filter_by(id=req.product_id, is_active=True).first()
            if not product:
                raise HTTPException(status_code=400, detail="Product not found")

            order = self.sess.query(Order).filter_by(id=req.orderId, is_active=True).first()
            if not order:
                raise HTTPException(status_code=400, detail="Order not found")

            new_order_item = OrderItem(**req.__dict__)
            order.price += product.price
            order.discount_price += product.price
            self.sess.add(new_order_item)
            self.sess.commit()

            logger.info(f"Inserted OrderItem with ID: {new_order_item.id}")
            return new_order_item

        except HTTPException:
            raise

        except Exception as e:
            self.sess.rollback()
            logger.error(f"Error inserting OrderItem: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
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
