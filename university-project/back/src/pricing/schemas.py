from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr, constr, conint


class PricingSchema(BaseModel):
    id: Optional[str] = None
    season_name: str
    start_time: datetime
    end_time: datetime
    peak_start_time: datetime
    peak_end_time: datetime
    general_price: int
    peak_price: int