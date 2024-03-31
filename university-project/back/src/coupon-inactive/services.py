# from typing import List
# from uuid import UUID
#
# from fastapi import Depends, status, HTTPException
# from sqlalchemy.orm import Session
#
# from ..core.schemas import Error
# from ..db.db import sess_db
# from .models import Coupon
# from .schemas import CouponReq, CouponUpdate
#
#
# class CouponService:
#     def __init__(self, db: Session):
#         self.db = db
#
#     def create_coupon(self, coupon_input: CouponReq):
#         """Create a new coupon-inactive."""
#
#         new_coupon = Coupon(**coupon_input.dict())
#         try:
#             self.db.add(new_coupon)
#             self.db.commit()
#         except:
#             self.db.rollback()
#         return new_coupon
#
#     def get_coupon_by_id(self, coupon_id: UUID):
#         """Retrieve a coupon-inactive by its ID."""
#
#         coupon = self.db.query(Coupon).filter_by(id=coupon_id).first()
#         if not coupon:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=Error(
#                     message="Coupon not found",
#                     code=404,
#                 ).dict(),
#             )
#         return coupon
#
#     def get_all_coupons(self) -> List[Coupon]:
#         """Retrieve all coupons."""
#
#         coupons = self.db.query(Coupon).all()
#         return coupons
#
#     def update_coupon(self, coupon_id: UUID, coupon_input: CouponUpdate):
#         """Update a coupon-inactive with patch update."""
#         coupon = self.get_coupon_by_id(coupon_id)
#
#         if coupon:
#             for field, value in coupon_input.dict(exclude_unset=True).items():
#                 setattr(coupon, field, value)
#
#             self.db.commit()
#             self.db.refresh(coupon)
#
#         return coupon
#
#     def delete_coupon(self, coupon_id: UUID):
#         """Delete a coupon-inactive by its ID."""
#         coupon = self.get_coupon_by_id(coupon_id)
#         if coupon:
#             self.db.delete(coupon)
#             self.db.commit()
#
#
# def get_coupon_service(db: Session = Depends(sess_db)) -> CouponService:
#     """Dependency to get an instance of the CouponService."""
#     return CouponService(db)
