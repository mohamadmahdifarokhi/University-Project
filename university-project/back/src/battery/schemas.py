from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr, constr, conint


class BatterySchema(BaseModel):
    id: Optional[str] = None
    user_id: str
    solar_panel_id: str
    saved_energy: int
    sold_energy: int

