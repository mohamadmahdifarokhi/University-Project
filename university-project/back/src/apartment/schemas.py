from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr, constr, conint


class ApartmentSchemaGet(BaseModel):
    id: Optional[str] = None
    apartment_no: int
    admin_id: str
    block_no: int

class ApartmentSchemacreate(BaseModel):
    id: Optional[str] = None
    apartment_no: int
    admin_id: str
    block_no: int

