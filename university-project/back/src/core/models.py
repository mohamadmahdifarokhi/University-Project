import pytz
from datetime import datetime
from fastapi_storages.integrations.sqlalchemy import ImageType
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


@declarative_mixin
class BaseModel:
    """
    Base model class with common fields for timestamping and soft deletion.

    Attributes:
        created (DateTime): The timestamp indicating the creation time.
        last_updated (DateTime): The timestamp indicating the last update time.
        deleted_at (DateTime): The timestamp indicating the deletion time.
        restored_at (DateTime): The timestamp indicating the restoration time.
        is_deleted (Boolean): A flag indicating if the record is marked as deleted.
        is_active (Boolean): A flag indicating if the record is active.

    Methods:
        __init__: Initializes the base model with optional keyword arguments.
    """
    __abstract__ = True

    created = Column(DateTime(timezone=True), default=datetime.now(pytz.utc), nullable=False)
    last_updated = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.utc), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    restored_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
