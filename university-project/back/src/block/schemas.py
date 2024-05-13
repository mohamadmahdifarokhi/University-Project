from datetime import datetime
from typing import List, Optional, Annotated
from pydantic import UUID4, BaseModel, EmailStr, constr, conint
from bson import ObjectId

from src.auth.schemas import ObjectIdPydanticAnnotation


class BlockSchemaGet(BaseModel):
    id: Optional[str] = None
    user_id: str
    apartment_id: str
    unit: int
    area: str

class BlockSchemaCreate1(BaseModel):
    id: Optional[str] = None
    # user_id: str
    apartment_no: int
    unit: int
    area: str

class BlockSchemaCreate(BaseModel):
    id: Optional[str] = None
    user_id: str
    apartment_id: str
    unit: int
    area: str