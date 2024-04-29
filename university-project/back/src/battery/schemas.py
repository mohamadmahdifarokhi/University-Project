from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr, constr, conint


class BatterySchema(BaseModel):
    id: Optional[str] = None
    user_id: str
    solar_panel_id: str
    saved_energy: int
    sold_energy: int
    status: str
    email: str

class BatteryAddSchema(BaseModel):
    id: Optional[str] = None
    saved_energy: int
    sold_energy: int

