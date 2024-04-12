from typing import Type
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Product


class ProductService:
    def __init__(self, sess: Session):
        self.sess: Session = sess

    # def create_product(self, name, price, discount_price, count, category_id, photo, description):
    #     """Create a new product."""
    #     category = self.sess.query(Category).filter_by(id=category_id).first()
    #     if not category:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=Error(
    #                 message="Category not found",
    #                 code=404,
    #             ).dict(),
    #         )
    #     slug = generate_slug(name)
    #     photo = boto_client.upload_fileobj(photo)
    #     new_product = Product(name=name, price=price, discount_price=discount_price, count=count,
    #                           category_id=category_id, photo=photo, description=description, slug=slug)
    #     self.sess.add(new_product)
    #     self.sess.commit()
    #     self.sess.refresh(new_product)
    #     return new_product

    def get_products(
            self,
            page: int,
            page_size: int,
    ) -> list[Type[Product]]:
        """
        Retrieve all products with pagination.

        Parameters:
        - page (int): Page number for pagination.
        - page_size (int): Number of products per page.

        Returns:
        - List[Product]: List of products.
        """
        start_index = (page - 1) * page_size
        products = (
            self.sess.query(Product)
            .filter_by(is_active=True)
            .offset(start_index)
            .limit(page_size)
            .all()
        )
        prices = read_prices()
        for product in products:
            product.price = float(prices["usd"]["value"]) * float(product.price)
        return products

    def get_not_active_products(
            self,
            page: int,
            page_size: int,
    ) -> list[Type[Product]]:
        """
        Retrieve not active all products with pagination.

        Parameters:
        - page (int): Page number for pagination.
        - page_size (int): Number of products per page.

        Returns:
        - List[Product]: List of products.
        """
        start_index = (page - 1) * page_size
        products = (
            self.sess.query(Product)
            .filter_by(is_active=False)
            .offset(start_index)
            .limit(page_size)
            .all()
        )
        prices = read_prices()
        for product in products:
            product.price = float(prices["usd"]["value"]) * float(product.price)
        return products

    def get_product_by_id(self, product_id: UUID) -> Type[Product]:
        """
        Retrieve a product by its ID.

        Parameters:
        - product_id (UUID): Product ID.

        Returns:
        - Product: Retrieved product.

        Raises:
        - HTTPException: If the product is not found.
        """
        product = (
            self.sess.query(Product).filter_by(id=product_id, is_active=True).first()
        )
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        prices = read_prices()
        product.price = float(prices["usd"]["value"]) * float(product.price)
        return product

    def get_product_by_slug(self, product_slug: str) -> Type[Product]:
        """
        Retrieve a product by its slug.

        Parameters:
        - product_slug (str): Product slug.

        Returns:
        - Product: Retrieved product.

        Raises:
        - HTTPException: If the product is not found.
        """
        product = (
            self.sess.query(Product).filter_by(slug=product_slug, is_active=True).first()
        )
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        prices = read_prices()
        product.price = float(prices["usd"]["value"]) * float(product.price)
        return product
    # def search_products(
    #         self,
    #         category_id: UUID = None,
    #         search: str = None,
    #         page: Optional[int] = Query(
    #             1,
    #             ge=1,
    #             description="Page number for pagination.",
    #         ),
    #         page_size: Optional[int] = Query(
    #             10,
    #             ge=1,
    #             description="Number of products per page.",
    #         ),
    # ) -> ProductPagination:
    #     """Search products by category and keyword with pagination."""
    #     if search is None:
    #         query = (
    #             self.sess.query(Product)
    #             .filter_by(is_active=True)
    #             .order_by(Product.created.desc())
    #         )
    #     else:
    #         query = self.sess.query(Product).filter(
    #             Product.is_active == True,
    #             (
    #                     Product.description.ilike(f"%{search}%")
    #                     | Product.name.ilike(f"%{search}%")
    #             ),
    #         )
    # 
    #     if category_id is None:
    #         total_products = query.count()
    #         products = query.offset((page - 1) * page_size).limit(page_size).all()
    #     else:
    #         category = (
    #             self.sess.query(Category)
    #             .filter_by(id=category_id, is_active=True)
    #             .first()
    #         )
    #         if not category:
    #             raise HTTPException(
    #                 status_code=status.HTTP_404_NOT_FOUND,
    #                 detail=Error(
    #                     message="Category not found",
    #                     code=404,
    #                 ).dict(),
    #             )
    # 
    #         filtered_categories = [category]
    #         if category.parent:
    #             filtered_categories += (
    #                 self.sess.query(Category).filter_by(parent=category).all()
    #             )
    #         else:
    #             child_categories = (
    #                 self.sess.query(Category).filter_by(parent=category).all()
    #             )
    #             filtered_categories += child_categories
    # 
    #         filtered_categories_ids = [cat.id for cat in filtered_categories]
    # 
    #         total_products = query.filter(
    #             Product.category_id.in_(filtered_categories_ids)
    #         ).count()
    #         products = (
    #             query.filter(Product.category_id.in_(filtered_categories_ids))
    #             .offset((page - 1) * page_size)
    #             .limit(page_size)
    #             .all()
    #         )
    # 
    #     product_res_list = [
    #         ProductRes(
    #             id=product.id,
    #             name=product.name,
    #             description=product.description,
    #             price=product.price,
    #             discount_price=product.discount_price,
    #             count=product.count,
    #             category_id=product.category_id,
    #         )
    #         for product in products
    #     ]
    #     return ProductPagination(
    #         total=total_products,
    #         page=page,
    #         page_size=page_size,
    #         products=product_res_list,
    #     )

    # def update_product(self, product_id: UUID, name=None, price=None, discount_price=None, count=None,
    # category_id=None, photo=None, description=None): """Update a product with patch update.""" product =
    # self.get_product_by_id(product_id)
    # 
    #     if product:
    #         update_data = {}
    # 
    #         if name is not None:
    #             update_data['name'] = name
    # 
    #         if price is not None:
    #             update_data['price'] = price
    # 
    #         if discount_price is not None:
    #             update_data['discount_price'] = discount_price
    # 
    #         if count is not None:
    #             update_data['count'] = count
    # 
    #         if category_id is not None:
    #             update_data['category_id'] = category_id
    # 
    #         if photo is not None:
    #             # Upload the file only if a new photo is provided
    #             uploaded_photo = boto_client.upload_fileobj(photo)
    #             update_data['photo'] = uploaded_photo
    # 
    #         if description is not None:
    #             update_data['description'] = description
    # 
    #         for field, value in update_data.items():
    #             setattr(product, field, value)
    # 
    #         product.last_updated = func.now()
    #         self.sess.commit()
    #         self.sess.refresh(product)
    # 
    #     return product

    # def delete_product(self, product_id: UUID):
    #     """Delete a product by its ID."""
    #     product = self.get_product_by_id(product_id)
    #     if product:
    #         self.sess.delete(product)
    #         self.sess.commit()
