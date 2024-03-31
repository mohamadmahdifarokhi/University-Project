from datetime import datetime
from pydantic import BaseModel


class BaseModelResponse(BaseModel):
    """
    Response schema for the BaseModel.

    Represents a response containing the creator, created timestamp, and last_updated timestamp.

    Attributes:
        created (datetime): The timestamp indicating the creation time.
        last_updated (datetime | None): The timestamp indicating the last update time.
        deleted_at (datetime | None): The timestamp indicating the deletion time.
        restored_at (datetime | None): The timestamp indicating the restoration time.
        is_deleted (bool): A flag indicating if the record is marked as deleted.
        is_active (bool): A flag indicating if the record is active.

    Config:
        from_attributes (bool): A Pydantic configuration to indicate attribute-based instantiation.
    """
    created: datetime
    last_updated: datetime | None = None
    deleted_at: datetime | None = None
    restored_at: datetime | None = None
    is_deleted: bool
    is_active: bool

    class Config:
        from_attributes = True
