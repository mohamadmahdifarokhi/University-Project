from pydantic import UUID4, BaseModel


# class CategoryReq(BaseModel):
#     """
#     Pydantic model for creating a category.
#
#     Inherits from BaseModel.
#     """
#     name: str
#     parent_id: UUID4 | None = None


class CategoryRes(BaseModel):
    """
    Pydantic model for the response of a category.

    Inherits from BaseModel.

    Attributes:
        name (dict): The name of the category.
        photo (str): The S3 link to the category's photo.
        parent_id (UUID4 | None): The unique identifier of the parent category, if any.
    """
    id: UUID4
    name: dict
    photo: str
    parent_id: UUID4 | None = None


# class CategoryUpdate(BaseModel):
#     """
#     Pydantic model for updating a category.
#
#     Inherits from BaseModel.
#     """
#     name: str = None
#     parent_id: UUID4 | None = None
