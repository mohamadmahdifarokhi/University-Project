# from typing import List
# from uuid import UUID
#
# from fastapi import APIRouter, Depends, HTTPException, status
#
# from .schemas import CouponReq, CouponRes, CouponUpdate
# from .services import CouponService, get_coupon_service
#
# router = APIRouter(tags=["Coupon"])
#
#
# @router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=CouponRes,
#     responses={
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def create_coupon_route(
#     coupon_input: CouponReq,
#     coupon_service: CouponService = Depends(get_coupon_service),
# ):
#     """Create a new coupon-inactive."""
#     new_coupon = coupon_service.create_coupon(coupon_input)
#     return new_coupon
#
#
# @router.get(
#     "/",
#     status_code=status.HTTP_200_OK,
#     response_model=List[CouponRes],
# )
# def get_coupons_route(
#     coupon_service: CouponService = Depends(get_coupon_service),
# ):
#     """Retrieve all coupons."""
#     coupons = coupon_service.get_all_coupons()
#     return coupons
#
#
# @router.get(
#     "/{coupon_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=CouponRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Coupon not found"},
#     },
# )
# def get_coupon_by_id_route(
#     coupon_id: UUID,
#     coupon_service: CouponService = Depends(get_coupon_service),
# ):
#     """Retrieve a coupon-inactive by its ID."""
#     coupon = coupon_service.get_coupon_by_id(coupon_id)
#     return coupon
#
#
# @router.patch(
#     "/{coupon_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=CouponRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Coupon not found"},
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def update_coupon_route(
#     coupon_id: UUID,
#     coupon_input: CouponUpdate,
#     coupon_service: CouponService = Depends(get_coupon_service),
# ):
#     """Partially update a coupon-inactive."""
#     updated_coupon = coupon_service.update_coupon(coupon_id, coupon_input)
#     return updated_coupon
#
#
# @router.delete(
#     "/{coupon_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Coupon not found"},
#     },
# )
# def delete_coupon_route(
#     coupon_id: UUID,
#     coupon_service: CouponService = Depends(get_coupon_service),
# ):
#     """Delete a coupon-inactive by its ID."""
#     coupon_service.delete_coupon(coupon_id)
#     return None
