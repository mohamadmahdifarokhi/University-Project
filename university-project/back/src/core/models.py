from typing import Optional

import pytz
from datetime import datetime
from fastapi_storages.integrations.sqlalchemy import ImageType
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.orm import declarative_mixin
from src.core.bucket import boto_client


class S3ImageType(ImageType):
    """
    Custom SQLAlchemy type for storing S3 image links.

    Inherits from fastapi_storages.integrations.sqlalchemy.ImageType.
    """

    def process_result_value(self, value, dialect):
        """
        Process the result value by generating an S3 link.

        Args:
            value: The stored value in the database.
            dialect: The SQLAlchemy dialect.

        Returns:
            str: The S3 link.
        """
        return boto_client.get_path(value) if value is not None else None

class BaseModel(PydanticBaseModel):
    """
    Pydantic base model class with common fields for timestamping and soft deletion.

    Attributes:
        created (datetime): The timestamp indicating the creation time.
        last_updated (Optional[datetime]): The timestamp indicating the last update time.
        deleted_at (Optional[datetime]): The timestamp indicating the deletion time.
        restored_at (Optional[datetime]): The timestamp indicating the restoration time.
        is_deleted (bool): A flag indicating if the record is marked as deleted.
        is_active (bool): A flag indicating if the record is active.
    """

    created: datetime
    last_updated: Optional[datetime]
    deleted_at: Optional[datetime]
    restored_at: Optional[datetime]
    is_deleted: bool
    is_active: bool

    class Config:
        orm_mode = True

