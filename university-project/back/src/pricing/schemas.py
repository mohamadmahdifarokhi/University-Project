from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr, constr, conint


class PricingSchema(BaseModel):
    id: Optional[str]
    device_id: str
    start_time: datetime
    end_time: datetime
    price: int
    peak_price: int