from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.params import Query
from sqlalchemy.orm import Session

from .schemas import CategoryRes
from .services import CategoryService
from ..db.db import sess_db

router = APIRouter(tags=["Categories"])


# @router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=CategoryRes,
#     responses={
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     })
# def create_category_route(
#         name: Annotated[str, Form()],
#         photo: Annotated[UploadFile, File()],
#         parent_id: Annotated[str, Form()] = None,
#         category_service: CategoryService = Depends(get_category_service),
# ):
#     """Create a new category."""
#     new_category = category_service.create_category(name, photo, parent_id)
#     print(new_category.__dict__)
#     return new_category.__dict__


# @router.get(
#     "/{category_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=CategoryRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Category not found"},
#     },
# )
# def get_category_by_id_route(
#         category_id: UUID,
#         category_service: CategoryService = Depends(get_category_service),
# ):
#     """Retrieve a category by its ID."""
#     category = category_service.get_category_by_id(category_id)
#     return category

@router.get(
    "",
    response_model=List[CategoryRes],
    status_code=status.HTTP_200_OK,
)
def get_all_categories_route(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sess: Session = Depends(sess_db),
):
    """
    Retrieve all categories with pagination.

    Args:
        page (int): The page number.
        page_size (int): The number of items per page.
        sess (Session): SQLAlchemy database session.

    Returns:
        List[CategoryRes]: List of CategoryRes objects.
    """
    categories = CategoryService(sess).get_all_categories(page, page_size)
    return categories

# @router.patch(
#     "/{category_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=CategoryRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Category not found"},
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def update_category_route(
#         category_id: UUID,
#         name: Annotated[str, Form()] = None,
#         photo: Annotated[UploadFile, File()] = None,
#         parent_id: Annotated[str, Form()] = None,
#         category_service: CategoryService = Depends(get_category_service),
# ):
#     """Partially update a category."""
#     updated_category = category_service.update_category(category_id, name, photo, parent_id)
#     print(updated_category.__dict__)
#     return updated_category


# @router.delete(
#     "/{category_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Category not found"},
#     },
# )
# def delete_category_route(
#         category_id: UUID,
#         category_service: CategoryService = Depends(get_category_service),
# ):
#     """Delete a category by its ID."""
#     category_service.delete_category(category_id)
#     return None
