# from uuid import UUID
#
# from fastapi import Depends, HTTPException, status
# from sqlalchemy.orm import Session
#
# from ..core.schemas import Error
# from ..db.db import sess_db
# from .models import WishList, WishListItem
# from .schemas import WishListItemReq, WishListItemUpdate, WishListReq, WishListUpdate
#
#
# class WishListService:
#     def __init__(self, db: Session):
#         self.db = db
#
#     def create_wishlist(self, wishlist_input: WishListReq):
#         """Create a new wishlist-inactive."""
#
#         new_wishlist = WishList(**wishlist_input.dict())
#         self.db.add(new_wishlist)
#         self.db.commit()
#         self.db.refresh(new_wishlist)
#         return new_wishlist
#
#     def get_wishlist_by_id(self, wishlist_id: UUID):
#         """Retrieve a wishlist-inactive by its ID."""
#
#         wishlist-inactive = self.db.query(WishList).filter_by(id=wishlist_id).first()
#         if not wishlist-inactive:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=Error(
#                     message="Wishlist not found",
#                     code=404,
#                 ).dict(),
#             )
#         return wishlist-inactive
#
#     def update_wishlist(self, wishlist_id: UUID, wishlist_input: WishListUpdate):
#         """Update a wishlist-inactive with patch update."""
#         wishlist-inactive = self.get_wishlist_by_id(wishlist_id)
#
#         if wishlist-inactive:
#             for field, value in wishlist_input.dict(exclude_unset=True).items():
#                 setattr(wishlist-inactive, field, value)
#
#             self.db.commit()
#             self.db.refresh(wishlist-inactive)
#
#         return wishlist-inactive
#
#     def delete_wishlist(self, wishlist_id: UUID):
#         """Delete a wishlist-inactive by its ID."""
#         wishlist-inactive = self.get_wishlist_by_id(wishlist_id)
#         if wishlist-inactive:
#             self.db.delete(wishlist-inactive)
#             self.db.commit()
#
#
# def get_wishlist_service(db: Session = Depends(sess_db)) -> WishListService:
#     """Dependency to get an instance of the WishListService."""
#     return WishListService(db)
#
#
# class WishListItemService:
#     def __init__(self, db: Session):
#         self.db = db
#
#     def create_wishlist_item(self, wishlist_item_input: WishListItemReq):
#         """Create a new wishlist-inactive item."""
#
#         new_wishlist_item = WishListItem(**wishlist_item_input.dict())
#         try:
#             self.db.add(new_wishlist_item)
#             self.db.commit()
#         except:
#             self.db.rollback()
#         return new_wishlist_item
#
#     def get_wishlist_item_by_id(self, wishlist_item_id: UUID):
#         """Retrieve a wishlist-inactive item by its ID."""
#
#         wishlist_item = (
#             self.db.query(WishListItem).filter_by(id=wishlist_item_id).first()
#         )
#         return wishlist_item
#
#     def update_wishlist_item(
#         self, wishlist_item_id: UUID, wishlist_item_input: WishListItemUpdate
#     ):
#         """Update a wishlist-inactive item with patch update."""
#         wishlist_item = self.get_wishlist_item_by_id(wishlist_item_id)
#
#         if wishlist_item:
#             for field, value in wishlist_item_input.dict(exclude_unset=True).items():
#                 setattr(wishlist_item, field, value)
#
#             self.db.commit()
#             self.db.refresh(wishlist_item)
#
#         return wishlist_item
#
#     def delete_wishlist_item(self, wishlist_item_id: UUID):
#         """Delete a wishlist-inactive item by its ID."""
#         wishlist_item = self.get_wishlist_item_by_id(wishlist_item_id)
#         if wishlist_item:
#             self.db.delete(wishlist_item)
#             self.db.commit()
#
#
# def get_wishlist_item_service(db: Session = Depends(sess_db)) -> WishListItemService:
#     """Dependency to get an instance of the WishListItemService."""
#     return WishListItemService(db)
