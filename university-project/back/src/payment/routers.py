import os
import uuid

from fastapi import APIRouter, Depends, HTTPException
import requests
import json
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.cart.services import CartItemService
from src.auth.models import User
from src.auth.secures import get_current_user
from src.db.db import sess_db
from src.order.schemas import OrderReq, OrderItemReq
from src.order.services import OrderService, order_itemservice
from src.payment.schemas import PaymentVerification
from .utils import read_prices

from ..core.utils import redis_instance
from ..logger import logger
from ..product.models import Product
from ..product.services import ProductService

router = APIRouter(tags=["Payments"])


@router.post("/request")
async def initiate_payment_request(user: User = Depends(get_current_user)):
    """
    Initiates a payment request to ZarinPal.

    Args:
        user (User): The authenticated user.

    Returns:
        JSONResponse: The payment URL.

    Raises:
        HTTPException: If there's an issue with the ZarinPal request or response.
    """
    try:

        if not user.cart.cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        amount = sum([item.product.price - item.product.discount_price for item in user.cart.cart_items])
        for item in user.cart.cart_items:
            print(item.product.price - item.product.discount_price)
        amount_id = str(uuid.uuid4())
        prices = read_prices()
        amount = float(prices["usd"]["value"]) * float(amount) * 10
        redis_instance.set(amount_id, str(amount))

        req_data = {
            "merchant_id": os.getenv("MERCHANT"),
            "amount": 10000,
            # "amount": amount,
            "callback_url": f"{os.getenv('FRONTEND_SERVER_URL')}/payment/verify?Id={amount_id}",
            "description": os.getenv("DESCRIPTION"),
            "metadata": {"mobile": "09123456789", "email": user.email}
        }

        # Send the payment request to ZarinPal
        req_header = {"accept": "application/json", "content-type": "application/json"}
        req = requests.post(url=os.getenv("ZP_API_REQUEST"), data=json.dumps(req_data), headers=req_header)
        print(req.__dict__)
        # Check if there are any errors in the ZarinPal response
        req.raise_for_status()

        # Extract the authority for the payment
        authority = req.json().get('data', {}).get('authority')
        if not authority:
            raise HTTPException(status_code=400, detail="ZarinPal authority not found in response")

        # Redirect the user to the ZarinPal payment page
        payment_url = os.getenv("ZP_API_STARTPAY").format(authority=str(authority))

        # Return the payment URL to the client
        return JSONResponse(content={"payment_url": payment_url})

    except HTTPException as e:
        logger.error(f"HTTPException in initiate_payment_request: {e}")
        raise
    except Exception as e:
        logger.error(f"Error in initiate_payment_request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/verify")
async def verify_payment(
        payment_verification: PaymentVerification,
        user: User = Depends(get_current_user),
        sess: Session = Depends(sess_db)
):
    """
    Verifies a payment with ZarinPal and processes the order.

    Args:
        payment_verification (PaymentVerification): The payment verification data.
        user (User): The authenticated user.
        sess (Session): The SQLAlchemy database session.

    Returns:
        JSONResponse: The payment verification result.

    Raises:
        HTTPException: If there's an issue with the ZarinPal verification request or response.
    """
    try:
        # amount = sum(
        #     [item.product.price - item.product.discount_price
        #      for item in user.cart.cartItem])

        authority = payment_verification.authority
        status = payment_verification.status
        amount_id = payment_verification.id

        amount = redis_instance.get(amount_id)

        if status != 'OK':
            return JSONResponse(content={"status": "failure", "message": "Transaction failed or canceled by the user"})

        # Prepare the payment verification data
        req_data = {
            "merchant_id": os.getenv("MERCHANT"),
            "amount": float(10000),
            # "amount": float(amount),
            "authority": authority
        }

        # Send the payment verification request to ZarinPal
        req_header = {"accept": "application/json", "content-type": "application/json"}
        req = requests.post(url=os.getenv("ZP_API_VERIFY"), data=json.dumps(req_data), headers=req_header)

        # Check if there are any errors in the ZarinPal response
        req.raise_for_status()
        t_status = req.json().get('data', {}).get('code')
        if t_status == 100:
            order_req = OrderReq(
                user_id=user.id,
                transaction_id=str(req.json().get('data', {}).get('ref_id')),
                price=amount,
                discount_price=0,
                status='not_processed'
            )
            new_order = OrderService(sess).insert(order_req)
            for cart_item in user.cart.cart_items:
                order_item_req = OrderItemReq(
                    name=cart_item.product.name,
                    price=cart_item.product.price,
                    discount_price=cart_item.product.discount_price,
                    email=cart_item.email,
                    password=cart_item.password,
                    description=cart_item.description,
                    status='not_processed',
                    orderId=new_order.id,
                    product_id=cart_item.product_id,
                )

                # Create the OrderItem using the orderItem_service
                order_itemservice(sess).insert(order_item_req)
                product = (
                    sess.query(Product).filter_by(id=cart_item.product_id).first()
                )
                product.count -= 1
                sess.commit()
                CartItemService(sess).delete(cart_item.id, user)
            redis_instance.delete(amount_id)
            return JSONResponse(content={"status": "success", "message": "Payment was successful"})
        elif t_status == 101:
            # Transaction is submitted
            redis_instance.delete(amount_id)
            return JSONResponse(content={"status": "submitted", "message": req.json().get('data', {}).get('message')})
        else:
            # Transaction failed
            redis_instance.delete(amount_id)
            return JSONResponse(content={"status": "failure", "message": req.json().get('data', {}).get('message')})
    except HTTPException as e:
        logger.error(f"HTTPException in verify_payment: {e}")
        raise
    except Exception as e:
        logger.error(f"Error in verify_payment: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
