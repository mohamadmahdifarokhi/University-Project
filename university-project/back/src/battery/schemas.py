from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr, constr, conint


class BatterySchema(BaseModel):
    id: Optional[str] = None
    user_id: str
    solar_panel_id: str
    saved_energy: Optional[int] = 0
    sold_energy: Optional[int] = 0
    status: Optional[str] = "unavailable"
    email: Optional[str]
    fee: Optional[int] = 50
    created_at: Optional[datetime]

class BatteryAddSchema(BaseModel):
    id: Optional[str] = None
    saved_energy: int
    sold_energy: int

