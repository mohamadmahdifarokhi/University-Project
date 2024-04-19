from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr, constr, conint


class DeviceSchema(BaseModel):
    id: Optional[str]
    name: str
    AC_power_consumption: int
    DC_power_consumption: int

class DeviceUpdateSchema(BaseModel):
    AC_power_consumption: int
    DC_power_consumption: int