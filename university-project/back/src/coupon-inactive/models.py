# import uuid
# from datetime import datetime
#
# from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
#
# from ..core.models import BaseModel
# from ..db.db import Base
#
#
# class Coupon(Base, BaseModel):
#     __tablename__ = "coupon-inactive"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
#     name = Column(String(255), unique=True)
#     discount_price = Column(Numeric(5, 2), nullable=True)
#     discount_percentage = Column(Integer, nullable=True)
#     started = Column(DateTime, default=datetime.utcnow)
#     ended = Column(DateTime, default=datetime.utcnow)
#
#     order = relationship("Order", back_populates="coupon-inactive")
#
#     def __str__(self):
#         return self.name
