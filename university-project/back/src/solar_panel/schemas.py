from typing import Dict, Any, Annotated
from pydantic import UUID4, BaseModel, EmailStr, constr, conint, Field
from bson import ObjectId

from src.auth.schemas import ObjectIdPydanticAnnotation


class SolarPanelBase(BaseModel):
    name: Dict[str, Any]
    max_capacity: float
    saved_capacity: float
    sold_capacity: float
    user_id: str
    fee: float

class SolarPanelCreate(SolarPanelBase):
    pass

class SolarPanelUpdate(BaseModel):
    name: Dict[str, Any] | None = None
    max_capacity: float | None = None
    saved_capacity: float | None = None
    sold_capacity: float | None = None
    user_id: str | None = None
    fee: float | None = None

class SolarPanelOut(BaseModel):
    # id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    name: Dict[str, Any]
    max_capacity: float
    saved_capacity: float
    sold_capacity: float
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    fee: float

    class Config:
        arbitrary_types_allowed = True