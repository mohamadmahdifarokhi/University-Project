# from datetime import datetime
# from typing import List, Optional
#
# from pydantic import UUID4, BaseModel
#
#
# class CouponReq(BaseModel):
#     name: str
#     discount_price: float = None
#     discount_percentage: int = None
#     started: datetime = None
#     ended: datetime = None
#
#
# class CouponRes(BaseModel):
#     id: UUID4
#     name: str
#     discount_price: float = None
#     discount_percentage: int = None
#     started: datetime
#     ended: datetime
#
#
# class CouponUpdate(BaseModel):
#     name: str = None
#     discount_price: float = None
#     discount_percentage: int = None
#     started: datetime = None
#     ended: datetime = None
