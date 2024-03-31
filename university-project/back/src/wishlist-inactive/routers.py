# from uuid import UUID
#
# from fastapi import APIRouter, Depends, HTTPException, status
#
# from .schemas import (
#     WishListItemReq,
#     WishListItemRes,
#     WishListItemUpdate,
#     WishListReq,
#     WishListRes,
#     WishListUpdate,
# )
# from .services import (
#     WishListItemService,
#     WishListService,
#     get_wishlist_item_service,
#     get_wishlist_service,
# )
#
# router = APIRouter(tags=["Wishlist"])
#
#
# @router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=WishListRes,
#     responses={
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def create_wishlist_route(
#     wishlist_input: WishListReq,
#     wishlist_service: WishListService = Depends(get_wishlist_service),
# ):
#     """Create a new wishlist-inactive."""
#     new_wishlist = wishlist_service.create_wishlist(wishlist_input)
#     return new_wishlist
#
#
# @router.get(
#     "/{wishlist_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=WishListRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "WishList not found"},
#     },
# )
# def get_wishlist_by_id_route(
#     wishlist_id: UUID,
#     wishlist_service: WishListService = Depends(get_wishlist_service),
# ):
#     """Retrieve a wishlist-inactive by its ID."""
#     wishlist-inactive = wishlist_service.get_wishlist_by_id(wishlist_id)
#     return wishlist-inactive
#
#
# @router.patch(
#     "/{wishlist_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=WishListRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "WishList not found"},
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def update_wishlist_route(
#     wishlist_id: UUID,
#     wishlist_input: WishListUpdate,
#     wishlist_service: WishListService = Depends(get_wishlist_service),
# ):
#     """Partially update a wishlist-inactive."""
#     updated_wishlist = wishlist_service.update_wishlist(wishlist_id, wishlist_input)
#     return updated_wishlist
#
#
# @router.delete(
#     "/{wishlist_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "WishList not found"},
#     },
# )
# def delete_wishlist_route(
#     wishlist_id: UUID,
#     wishlist_service: WishListService = Depends(get_wishlist_service),
# ):
#     """Delete a wishlist-inactive by its ID."""
#     wishlist_service.delete_wishlist(wishlist_id)
#     return None
#
#
# @router.post(
#     "/item/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=WishListItemRes,
#     responses={
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def create_wishlist_item_route(
#     wishlist_item_input: WishListItemReq,
#     wishlist_item_service: WishListItemService = Depends(get_wishlist_item_service),
# ):
#     """Create a new wishlist-inactive item."""
#     new_wishlist_item = wishlist_item_service.create_wishlist_item(wishlist_item_input)
#     return new_wishlist_item
#
#
# @router.get(
#     "/item/{wishlist_item_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=WishListItemRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "WishList item not found"},
#     },
# )
# def get_wishlist_item_by_id_route(
#     wishlist_item_id: UUID,
#     wishlist_item_service: WishListItemService = Depends(get_wishlist_item_service),
# ):
#     """Retrieve a wishlist-inactive item by its ID."""
#     wishlist_item = wishlist_item_service.get_wishlist_item_by_id(wishlist_item_id)
#     return wishlist_item
#
#
# @router.patch(
#     "/item/{wishlist_item_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=WishListItemRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "WishList item not found"},
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def update_wishlist_item_route(
#     wishlist_item_id: UUID,
#     wishlist_item_input: WishListItemUpdate,
#     wishlist_item_service: WishListItemService = Depends(get_wishlist_item_service),
# ):
#     """Partially update a wishlist-inactive item."""
#     updated_wishlist_item = wishlist_item_service.update_wishlist_item(
#         wishlist_item_id, wishlist_item_input
#     )
#     return updated_wishlist_item
#
#
# @router.delete(
#     "/item/{wishlist_item_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "WishList item not found"},
#     },
# )
# def delete_wishlist_item_route(
#     wishlist_item_id: UUID,
#     wishlist_item_service: WishListItemService = Depends(get_wishlist_item_service),
# ):
#     """Delete a wishlist-inactive item by its ID."""
#     wishlist_item_service.delete_wishlist_item(wishlist_item_id)
#     return None
