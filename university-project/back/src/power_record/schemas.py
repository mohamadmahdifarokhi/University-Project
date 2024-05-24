from datetime import datetime
from typing import List, Optional, Annotated
from pydantic import UUID4, BaseModel, EmailStr, constr, conint
from bson import ObjectId

from src.auth.schemas import ObjectIdPydanticAnnotation


class PowerRecordSchema(BaseModel):
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    device_name: str
    start_time: datetime
    end_time: datetime
    consumption: float

class PowerRecordAddSchema(BaseModel):
    device_name: str
    start_time: datetime
    end_time: datetime

class PowerRecordGetSchema(BaseModel):
    power_record_id: str
    device_name: str
    start_time: datetime
    end_time: datetime
    consumption: float