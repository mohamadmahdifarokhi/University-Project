from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any

class SolarPanel(BaseModel):
    id: str = Field(..., description="The unique identifier of the solar panel")
    name: Dict[str, Any] = Field(..., description="The name of the solar panel")
    max_capacity: float = Field(..., description="The maximum capacity of the solar panel")
    saved_capacity: float = Field(..., description="The amount of saved capacity of the solar panel")
    sold_capacity: float = Field(..., description="The amount of sold capacity of the solar panel")
    user_id: str = Field(..., description="The unique identifier of the user associated with the solar panel")
    fee: float = Field(..., description="The fee of the solar panel")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": {"brand": "BrandName", "model": "ModelName"},
                "max_capacity": 100.0,
                "saved_capacity": 50.0,
                "sold_capacity": 20.0,
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "fee": 10.0
            }
        }
