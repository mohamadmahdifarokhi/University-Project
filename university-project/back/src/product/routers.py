from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.params import Query
from sqlalchemy.orm import Session

from .schemas import ProductRes
from .services import ProductService
from ..db.db import sess_db

router = APIRouter(tags=["Products"])


# @router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=ProductRes,
#     responses={
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def create_product_route(
#         name: Annotated[str, Form()],
#         price: Annotated[float, Form()],
#         discount_price: Annotated[float, Form()],
#         count: Annotated[int, Form()],
#         category_id: Annotated[str, Form()],
#         photo: Annotated[UploadFile, File()],
#         description: Annotated[str, Form()] = None,
#         product_service: ProductService = Depends(get_product_service),
# ):
#     """Create a new product."""
#     new_product = product_service.create_product(name, price, discount_price, count, category_id, photo, description)
#     return new_product


# @router.get(
#     "/search/",
#     response_model=ProductPagination,
#     responses={
#         status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# def search_products_route(
#         category_id: UUID = None,
#         search: str = None,
#         page: Optional[int] = Query(
#             0,
#             ge=0,
#             description="Page number for pagination.",
#         ),
#         page_size: Optional[int] = Query(
#             10,
#             ge=1,
#             description="Number of products per page.",
#         ),
#         product_service: ProductService = Depends(get_product_service),
# ):
#     """Search products by category and keyword with pagination."""
#     return product_service.search_products(category_id, search, page, page_size)


# @router.get(
#     "/{product_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=ProductRes,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Product not found"},
#     },
# )
# def get_product_by_id_route(
#         product_id: UUID,
#         product_service: ProductService = Depends(get_product_service),
# ):
#     """Retrieve a product by its ID."""
#     product = product_service.get_product_by_id(product_id)
#     return product

@router.get(
    "/{product_slug}",
    response_model=ProductRes,
    status_code=status.HTTP_200_OK,
)
def get_product_by_slug_route(
        product_slug: str,
        sess: Session = Depends(sess_db),
):
    """
    Retrieve a product by its slug.

    Args:
        product_slug (str): The slug of the product.
        sess (Session): SQLAlchemy database session.

    Returns:
        ProductRes: Product response.
    """
    product = ProductService(sess).get_product_by_slug(product_slug)
    return product


@router.get(
    "",
    response_model=List[ProductRes],
    status_code=status.HTTP_200_OK,
)
def get_products_route(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        sess: Session = Depends(sess_db),
):
    """
    Retrieve all products with pagination.

    Args:
        page (int): The page number.
        page_size (int): The number of items per page.
        sess (Session): SQLAlchemy database session.

    Returns:
        List[ProductRes]: List of product responses.
    """
    products = ProductService(sess).get_products(page, page_size)
    return products


@router.get(
    "/isActivate/false",
    response_model=List[ProductRes],
    status_code=status.HTTP_200_OK,
)
def get_not_active_products_route(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        sess: Session = Depends(sess_db),
):
    """
    Retrieve not active all products with pagination.

    Args:
        page (int): The page number.
        page_size (int): The number of items per page.
        sess (Session): SQLAlchemy database session.

    Returns:
        List[ProductRes]: List of product responses.
    """
    products = ProductService(sess).get_not_active_products(page, page_size)
    return products

# @router.patch( "/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductRes, responses={
# status.HTTP_404_NOT_FOUND: {"description": "Product not found"}, status.HTTP_400_BAD_REQUEST: {"description": "Bad
# request"}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}, },
# ) def update_product_route( product_id: UUID, name: Annotated[str, Form()] = None, price: Annotated[float,
# Form()] = None, discount_price: Annotated[float, Form()] = None, count: Annotated[int, Form()] = None, category_id:
# Annotated[str, Form()] = None, photo: Annotated[UploadFile, File()] = None, description: Annotated[str,
# Form()] = None, product_service: ProductService = Depends(get_product_service), ): """Partially update a
# product.""" updated_product = product_service.update_product(product_id, name, price, discount_price, count,
# category_id, photo, description) return updated_product


# @router.delete(
#     "/{product_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Product not found"},
#     },
# )
# def delete_product_route(
#         product_id: UUID,
#         product_service: ProductService = Depends(get_product_service),
# ):
#     """Delete a product by its ID."""
#     product_service.delete_product(product_id)
#     return None
