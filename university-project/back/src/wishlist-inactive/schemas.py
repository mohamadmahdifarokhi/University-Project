# from typing import List
#
# from pydantic import UUID4, BaseModel
#
#
# class WishListReq(BaseModel):
#     user_id: UUID4
#
#
# class WishListRes(BaseModel):
#     id: UUID4
#     user_id: UUID4
#     cartItem: List = None
#
#
# class WishListUpdate(BaseModel):
#     user_id: UUID4 = None
#     cartItem: List = None
#
#
# class WishListItemReq(BaseModel):
#     cart_id: UUID4
#     product_id: UUID4
#     count: int
#
#
# class WishListItemRes(BaseModel):
#     id: UUID4
#     cart_id: UUID4
#     product_id: UUID4
#     count: int
#
#
# class WishListItemUpdate(BaseModel):
#     cart_id: UUID4 = None
#     product_id: UUID4 = None
#     count: int = None
