from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr, constr, conint


class DeviceSchema(BaseModel):
    id: Optional[str] = None
    name: str
    AC_power_consumption: float
    DC_power_consumption: float

class DeviceUpdateSchema(BaseModel):
    AC_power_consumption: float
    DC_power_consumption: float