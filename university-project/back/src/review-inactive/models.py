# import uuid
#
# from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
#
# from ..core.models import BaseModel
# from ..db.db import Base
#
#
# class Review(Base, BaseModel):
#     __tablename__ = "review-inactive"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
#     is_reply = Column(Boolean, default=False)
#     head = Column(String(255))
#     body = Column(Text)
#     rating = Column(Float)
#
#     user = relationship("User", back_populates="review-inactive")
#     user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
#
#     product = relationship("Product", back_populates="review-inactive")
#     product_id = Column(UUID(as_uuid=True), ForeignKey("product.id"))
#
#     reply = relationship("Review", remote_side=[id], back_populates="replies")
#     reply_id = Column(UUID(as_uuid=True), ForeignKey("review-inactive.id"))
#
#     replies = relationship("Review", remote_side=[reply_id], back_populates="reply")
