# from typing import List
# from uuid import UUID
#
# from fastapi import APIRouter, Depends, status
#
# from .schemas import ReviewReq, ReviewRes, ReviewUpdate
# from .services import ReviewService, get_review_service
#
# router = APIRouter(tags=["Review"])
#
#
# @router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=ReviewRes,
#     responses={
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def create_review_route(
#     review_input: ReviewReq,
#     review_service: ReviewService = Depends(get_review_service),
# ):
#     """Create a new review-inactive."""
#     new_review = review_service.create_review(review_input)
#     return new_review
#
#
# @router.get(
#     "/",
#     status_code=status.HTTP_200_OK,
#     response_model=List[ReviewRes],
# )
# def get_all_reviews_route(
#     review_service: ReviewService = Depends(get_review_service),
# ):
#     """Retrieve all reviews."""
#     reviews = review_service.get_all_reviews()
#     return reviews
#
#
# @router.get(
#     "/{review_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=ReviewRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Review not found"},
#     },
# )
# def get_review_by_id_route(
#     review_id: UUID,
#     review_service: ReviewService = Depends(get_review_service),
# ):
#     """Retrieve a review-inactive by its ID."""
#     review-inactive = review_service.get_review_by_id(review_id)
#     return review-inactive
#
#
# @router.get(
#     "/product/{product_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=List[ReviewRes],
# )
# def get_reviews_for_product_route(
#     product_id: UUID,
#     review_service: ReviewService = Depends(get_review_service),
# ):
#     """Retrieve all reviews for a product."""
#     reviews = review_service.get_reviews_for_product(product_id)
#     return reviews
#
#
# @router.get(
#     "/product/{product_id}/user/{user_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=List[ReviewRes],
# )
# def get_reviews_for_product_by_user_id_route(
#     product_id: UUID,
#     user_id: UUID,
#     review_service: ReviewService = Depends(get_review_service),
# ):
#     """Retrieve all reviews for a product by a specific user."""
#     reviews = review_service.get_reviews_for_product_by_user_id(product_id, user_id)
#     return reviews
#
#
# @router.patch(
#     "/{review_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=ReviewRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Review not found"},
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def update_review_route(
#     review_id: UUID,
#     review_input: ReviewUpdate,
#     review_service: ReviewService = Depends(get_review_service),
# ):
#     """Partially update a review-inactive."""
#     updated_review = review_service.update_review(review_id, review_input)
#     return updated_review
#
#
# @router.delete(
#     "/{review_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Review not found"},
#     },
# )
# def delete_review_route(
#     review_id: UUID,
#     review_service: ReviewService = Depends(get_review_service),
# ):
#     """Delete a review-inactive by its ID."""
#     review_service.delete_review(review_id)
#     return None
