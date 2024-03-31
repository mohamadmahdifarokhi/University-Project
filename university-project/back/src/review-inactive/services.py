# from typing import List, Type
# from uuid import UUID
#
# from fastapi import Depends, HTTPException, status
# from sqlalchemy.orm import Session
#
# from src.product.models import Product
#
# from ..auth.models import User
# from ..core.schemas import Error
# from ..db.db import sess_db
# from .models import Review
# from .schemas import ReviewReq, ReviewUpdate
#
#
# class ReviewService:
#     def __init__(self, db: Session):
#         self.db = db
#
#     def create_review(self, review_input: ReviewReq):
#         """Create a new review-inactive."""
#
#         user = self.db.query(User).filter_by(id=review_input.user_id).first()
#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=Error(
#                     message="User not found",
#                     code=404,
#                 ).dict(),
#             )
#
#         product = self.db.query(Product).filter_by(id=review_input.product_id).first()
#         if not product:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=Error(
#                     message="Product not found",
#                     code=404,
#                 ).dict(),
#             )
#
#         new_review = Review(**review_input.dict())
#         self.db.add(new_review)
#         self.db.commit()
#         self.db.refresh(new_review)
#         return new_review
#
#     def get_all_reviews(self) -> List[Type[Review]]:
#         """Retrieve all reviews."""
#         reviews = self.db.query(Review).all()
#         return reviews
#
#     def get_review_by_id(self, review_id: UUID):
#         """Retrieve a review-inactive by its ID."""
#         review-inactive = self.db.query(Review).filter_by(id=review_id).first()
#         if not review-inactive:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=Error(
#                     message="Review not found",
#                     code=404,
#                 ).dict(),
#             )
#         return review-inactive
#
#     def get_reviews_for_product(self, product_id: UUID) -> List[Type[Review]]:
#         """Retrieve all reviews for a product."""
#         product = self.db.query(Product).filter_by(id=product_id).first()
#         if not product:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=Error(
#                     message="Product not found",
#                     code=404,
#                 ).dict(),
#             )
#         reviews = (
#             self.db.query(Review)
#             .filter_by(product_id=product_id)
#             .order_by(Review.created.desc())
#             .all()
#         )
#         return reviews
#
#     def get_reviews_for_product_by_user_id(
#             self, product_id: UUID, user_id: UUID
#     ) -> List[Type[Review]]:
#         """Retrieve all reviews for a product by a specific user."""
#         user = self.db.query(User).filter_by(id=user_id).first()
#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=Error(
#                     message="User not found",
#                     code=404,
#                 ).dict(),
#             )
#
#         product = self.db.query(Product).filter_by(id=product_id).first()
#         if not product:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=Error(
#                     message="Product not found",
#                     code=404,
#                 ).dict(),
#             )
#
#         reviews = (
#             self.db.query(Review)
#             .filter_by(product_id=product_id, user_id=user_id)
#             .order_by(Review.created.desc())
#             .all()
#         )
#         return reviews
#
#     def update_review(self, review_id: UUID, review_input: ReviewUpdate):
#         """Update a review-inactive with patch update."""
#         review-inactive = self.get_review_by_id(review_id)
#
#         if review-inactive:
#             for field, value in review_input.dict(exclude_unset=True).items():
#                 setattr(review-inactive, field, value)
#
#             self.db.commit()
#             self.db.refresh(review-inactive)
#
#         return review-inactive
#
#     def delete_review(self, review_id: UUID):
#         """Delete a review-inactive by its ID."""
#         review-inactive = self.get_review_by_id(review_id)
#         if review-inactive:
#             self.db.delete(review-inactive)
#             self.db.commit()
#
#
# def get_review_service(db: Session = Depends(sess_db)) -> ReviewService:
#     """Dependency to get an instance of the ReviewService."""
#     return ReviewService(db)
