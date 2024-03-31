from pydantic import BaseModel, UUID4

from src.category.schemas import CategoryRes


# class ProductReq(BaseModel):
#     """
#     Request model for creating a new product.
#
#     Attributes:
#     - name (str): Name of the product.
#     - description (str, optional): Description of the product.
#     - price (float): Regular price of the product.
#     - discount_price (float, optional): Discounted price of the product.
#     - count (int, optional): Quantity of the product available in stock, default is 0.
#     - category_id (UUID4): UUID4 for the category of the product.
#     """
#
#     name: str
#     description: Optional[str] = None
#     price: float
#     discount_price: Optional[float] = None
#     count: int = 0
#     category_id: UUID4


class ProductRes(BaseModel):
    """
    Response model for retrieving product information.

    Attributes:
    - id (UUID4): Id of the product.
    - name (str): Name of the product.
    - slug (str): Slug for the product.
    - photo (str): Path or URL to the product photo.
    - description (str): Description of the product.
    - price (float): Regular price of the product.
    - discount_price (float): Discounted price of the product.
    - count (int): Quantity of the product available in stock.
    - category (CategoryRes): Information about the category of the product.
    """

    id: UUID4
    name: dict
    slug: str
    photo: str
    background: str
    logo: str
    description: dict
    price: float
    discount_price: float
    count: int
    category: CategoryRes


# class ProductUpdate(BaseModel):
#     """
#     Model for updating product information.
#
#     Attributes:
#     - name (str, optional): New name for the product.
#     - description (str, optional): New description for the product.
#     - price (float, optional): New regular price for the product.
#     - discount_price (float, optional): New discounted price for the product.
#     - count (int, optional): New quantity of the product available in stock.
#     - category_id (UUID4, optional): New UUID4 for the category of the product.
#     """
#
#     name: str = None
#     description: Optional[str] = None
#     price: float = None
#     discount_price: Optional[float] = None
#     count: int = None
#     category_id: UUID4 = None


# class ProductPagination(BaseModel):
#     """
#     Model for paginated product response.
#
#     Attributes:
#     - total (int): Total number of products.
#     - page (int): Current page number.
#     - page_size (int): Number of products per page.
#     - products (List[ProductRes]): List of product information for the current page.
#     """
#
#     total: int
#     page: int
#     page_size: int
#     products: List[ProductRes]


# class Scopes(BaseModel):
#     """
#     Model for handling OAuth2 scopes.
#
#     Attributes:
#     - scopes (List): List of scopes.
#     """
#
#     scopes: List
