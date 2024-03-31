# import uuid
#
# from sqlalchemy import Column, ForeignKey, Integer
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
#
# from ..core.models import BaseModel
# from ..db.db import Base
#
#
# class WishList(Base, BaseModel):
#     __tablename__ = "wishlist-inactive"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
#
#     user = relationship("User", back_populates="wishlist-inactive")
#     user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), unique=True)
#
#     wishlist_item = relationship("WishListItem", back_populates="wishlist-inactive")
#
#
# class WishListItem(Base, BaseModel):
#     __tablename__ = "wishlist_item"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
#     count = Column(Integer)
#
#     wishlist-inactive = relationship("WishList", back_populates="wishlist_item")
#     cart_id = Column(UUID(as_uuid=True), ForeignKey("wishlist-inactive.id"))
#
#     product = relationship("Product", back_populates="wishlist_item")
#     product_id = Column(UUID(as_uuid=True), ForeignKey("product.id"))
