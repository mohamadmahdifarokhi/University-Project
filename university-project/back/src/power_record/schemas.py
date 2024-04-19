from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr, constr, conint


class PowerRecordSchema(BaseModel):
    user_id: str 
    device_name: str
    start_time: datetime
    end_time: datetime
    consumption: int

class PowerRecordAddSchema(BaseModel):
    device_name: str
    start_time: datetime
    end_time: datetime
    consumption: int

class PowerRecordGetSchema(BaseModel):
    device_name: str
    start_time: datetime
    end_time: datetime
    consumption: int