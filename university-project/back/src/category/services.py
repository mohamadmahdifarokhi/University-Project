from typing import Type, List
from sqlalchemy.orm import Session
from .models import Category


class CategoryService:
    """
    Service class for managing Category-related operations.

    Attributes:
        sess (Session): The SQLAlchemy database session.
    """

    def __init__(self, sess: Session):
        self.sess: Session = sess

    # def create_category(self, name, photo, parent_id=None):
    #     """Create a new category."""
    #
    #     photo = boto_client.upload_fileobj(photo)
    #     new_category = Category(name=name, photo=photo, parent_id=parent_id)
    #     self.db.add(new_category)
    #     self.db.commit()
    #     self.db.refresh(new_category)
    #     return new_category

    # def get_category_by_id(self, category_id: UUID):
    #     """Retrieve a category by its ID."""
    #
    #     category = (
    #         self.db.query(Category).filter_by(id=category_id, is_active=True).first()
    #     )
    #     if not category:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=Error(
    #                 message="Category not found",
    #                 code=404,
    #             ).dict(),
    #         )
    #     return category

    def get_all_categories(self, page: int, page_size: int) -> List[Type[Category]]:
        """
        Retrieve all categories with pagination.

        Args:
            page (int): The page number.
            page_size (int): The number of items per page.

        Returns:
            List[Type[Category]]: A list of Category objects.
        """
        start_index = (page - 1) * page_size
        categories = (
            self.sess.query(Category)
            .filter_by(is_active=True)
            .offset(start_index)
            .limit(page_size)
            .all()
        )
        return categories

    # def update_category(self, category_id: UUID, name=None, photo=None, parent_id=None):
    #     """Update a category with patch update."""
    #     category = self.get_category_by_id(category_id)
    #
    #     if category:
    #         update_data = {}
    #
    #         if name is not None:
    #             update_data['name'] = name
    #
    #         if photo is not None:
    #             # Upload the file only if a new photo is provided
    #             uploaded_photo = boto_client.upload_fileobj(photo)
    #             update_data['photo'] = uploaded_photo
    #
    #         if parent_id is not None:
    #             update_data['parent_id'] = parent_id
    #
    #         for field, value in update_data.items():
    #             setattr(category, field, value)
    #
    #         self.db.commit()
    #         self.db.refresh(category)
    #
    #     return category

    # def delete_category(self, category_id: UUID):
    #     """Delete a category by its ID."""
    #     category = self.get_category_by_id(category_id)
    #     if category:
    #         self.db.delete(category)
    #         self.db.commit()
