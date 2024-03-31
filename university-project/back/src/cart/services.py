from typing import Type
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Cart, CartItem
from .schemas import CartItemReq
from ..auth.models import User
from ..logger import logger
from ..payment.utils import read_prices
from ..product.models import Product
from ..product.services import ProductService


class CartService:
    """
    Service class for handling Cart-related operations.

    Args:
        sess (Session): The SQLAlchemy database session.
    """

    def __init__(self, sess: Session):
        self.sess: Session = sess

    # def insert(self, user_id: UUID):
    #     """
    #     Insert a new cart for the user into the database.
    #
    #     Args:
    #         user_id (UUID): The ID of the user for whom the cart is created.
    #
    #     Returns:
    #         Cart: The inserted cart entity.
    #     """
    #     if self.get_by_user_id(user_id):
    #         raise HTTPException(status_code=400, detail="Cart for user already exists")
    #
    #     try:
    #         cart = Cart(user_id=user_id)
    #         self.sess.add(cart)
    #         self.sess.commit()
    #
    #         logger.info(f"Inserted Cart with ID: {cart.id} for User ID: {user_id}")
    #
    #         return cart
    #     except Exception as e:
    #         self.sess.rollback()
    #         logger.error(f"Insert operation failed: {e}")
    #         raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_by_user_id(self, user: User) -> Type[Cart]:
        """
        Retrieve cart with associated cart items and product details by user.

        Args:
            user (User): User model.

        Returns:
            Cart: Cart object.
        """
        try:
            cart = self.sess.query(Cart).filter_by(user_id=user.id, is_active=True).first()
            print(cart.cart_items)
            if not cart:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Cart not found for user with ID: {user.id}"
                )

            prices = read_prices()
            exist_products = []

            for cart_item in cart.cart_items:
                if cart_item.product.count <= 0:
                    self.sess.delete(cart_item)
            self.sess.commit()
            for cart_item in cart.cart_items:

                # print(cart_item.product.price)
                if cart_item.product not in exist_products:
                    cart_item.product.price = float(prices["usd"]["value"]) * float(cart_item.product.price)
                    exist_products.append(cart_item.product)
            return cart
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving cart for user: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    # def update(self, user_id: UUID, details) -> Type[Cart]:
    #     """
    #     Update a cart entity in the database.
    #
    #     Args:
    #         user_id (UUID): The ID of the user whose cart is to be updated.
    #         details: The details to be updated.
    #
    #     Returns:
    #         bool: True if the operation is successful, False otherwise.
    #     """
    #     try:
    #         cart = self.get_by_user_id(user_id)
    #         if not cart:
    #             raise HTTPException(status_code=400, detail="Cart for user not found")
    #
    #         for field, value in details.dict(exclude_unset=True).items():
    #             setattr(cart, field, value)
    #
    #         self._commit_or_rollback()
    #
    #         logger.info(f"Updated Cart with ID: {cart.id} for User ID: {user_id}")
    #     except NoResultFound:
    #         logger.error(f"Update operation failed: Cart for User ID {user_id} not found")
    #         raise HTTPException(status_code=400, detail="Cart not found")
    #     except IntegrityError as e:
    #         self.sess.rollback()
    #         logger.error(f"Update operation failed: {e}")
    #         raise HTTPException(status_code=400, detail="Error updating cart")
    #     except Exception as e:
    #         self.sess.rollback()
    #         logger.error(f"Update operation failed: {e}")
    #         raise HTTPException(
    #             status_code=500,
    #             detail="Failed to update the Cart record.")
    #     return cart


class CartItemService:
    """
    Service class for handling operations related to CartItem entities.
    """

    def __init__(self, sess: Session):
        self.sess: Session = sess

    def insert(self, req: CartItemReq, user: User) -> CartItem:
        """
        Insert a new CartItem into the database.

        Args:
            req (CartItemReq): Request model for creating a CartItem.
            user (User): User model.

        Returns:
            CartItem: Newly inserted CartItem.
        """
        try:
            if (req.email is None and req.password is not None) or \
                    (req.email is not None and req.password is None):
                raise HTTPException(
                    status_code=400,
                    detail="Either both email and password should be provided or neither."
                )

            product = (
                self.sess.query(Product).filter_by(id=req.product_id, is_active=True).first()
            )
            if product.count <= 0:
                raise HTTPException(status_code=400, detail="Product is out of stock")

            if len(user.cart.cart_items) >= 5:
                raise HTTPException(status_code=400, detail="Cannot add more than 5 items to the cart")

            cart_item = CartItem(cart_id=user.cart.id, **req.__dict__)
            self.sess.add(cart_item)
            self.sess.commit()

            logger.info(f"Inserted CartItem with ID: {cart_item.id}")
            prices = read_prices()
            cart_item.product.price = float(prices["usd"]["value"]) * float(cart_item.product.price)
            return cart_item

        except HTTPException:
            raise
        except Exception as e:
            self.sess.rollback()
            logger.error(f"Error inserting CartItem: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    # def update(self, cart_item_id: UUID, cart_item_update, user: User) -> Type[CartItem]:
    #     """
    #     Update a CartItem in the database.
    #
    #     Args:
    #         cart_item_id (UUID): UUID of the CartItem to be updated.
    #         cart_item_update: Update model for partially updating a CartItem.
    #         user (User): User model.
    #
    #     Returns:
    #         Optional[CartItem]: Updated CartItem if successful, None otherwise.
    #
    #     Raises:
    #         HTTPException: If the update fails, raise a 500 Internal Server Error exception.
    #     """
    #     try:
    #         cart_item = self.sess.query(CartItem).filter_by(id=cart_item_id, cart=user.cart).first()
    #         if not cart_item:
    #             raise HTTPException(status_code=404, detail=f"CartItem with ID {cart_item_id} not found")
    #         for field, value in cart_item_update.dict(exclude_unset=True).items():
    #             setattr(cart_item, field, value)
    #         self.sess.commit()
    #         logger.info(f"Updated CartItem with ID: {cart_item_id}")
    #         return cart_item
    #     except Exception as e:
    #         self.sess.rollback()
    #         logger.error(f"Update operation failed: {e}")
    #         raise HTTPException(status_code=500, detail="Internal Server Error")

    def delete(self, cart_item_id: UUID, user: User) -> bool:
        """
        Delete a CartItem from the database.

        Args:
            cart_item_id (UUID): UUID of the CartItem to be deleted.
            user (User): User model.

        Returns:
            bool: True if the deletion is successful.
        """
        try:
            cart_item = self.sess.query(CartItem).filter_by(id=cart_item_id, cart_id=user.cart.id,
                                                            is_active=True).first()
            if not cart_item:
                raise HTTPException(status_code=404, detail=f"CartItem with ID {cart_item_id} not found")
            self.sess.delete(cart_item)
            self.sess.commit()
            logger.info(f"Deleted CartItem with ID: {cart_item_id}")
            return True
        except HTTPException:
            raise
        except Exception as e:
            self.sess.rollback()
            logger.error(f"Error deleting CartItem: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
