from fastapi import APIRouter, HTTPException
from typing import List
from .schemas import SolarPanelCreate, SolarPanelOut, SolarPanelUpdate
from .services import SolarPanelService

router = APIRouter(tags=["Solar Panels"])

solar_panel_service = SolarPanelService()

@router.post("/solar-panels/create", response_model=SolarPanelOut)
async def create_solar_panel(solar_panel: SolarPanelCreate):
    """
    Create a new solar panel.
    """
    return solar_panel_service.create_solar_panel(solar_panel)

@router.get("/solar-panels/read", response_model=List[SolarPanelOut])
async def read_solar_panels(skip: int = 0, limit: int = 10):
    """
    Get a list of solar panels.
    """
    return solar_panel_service.get_solar_panels(skip=skip, limit=limit)

@router.get("/solar-panels/read/{solar_panel_id}", response_model=SolarPanelOut)
async def read_solar_panel(solar_panel_id: str):
    """
    Get a solar panel by ID.
    """
    solar_panel = solar_panel_service.get_solar_panel(solar_panel_id)
    if not solar_panel:
        raise HTTPException(status_code=404, detail="Solar panel not found")
    return solar_panel

@router.patch("/solar-panels/update/{solar_panel_id}", response_model=SolarPanelOut)
async def update_solar_panel(solar_panel_id: str, solar_panel_update: SolarPanelUpdate):
    """
    Update a solar panel.
    """
    updated_solar_panel = solar_panel_service.update_solar_panel(solar_panel_id, solar_panel_update)
    if not updated_solar_panel:
        raise HTTPException(status_code=404, detail="Solar panel not found")
    return updated_solar_panel

@router.delete("/solar-panels/delete/{solar_panel_id}", response_model=SolarPanelOut)
async def delete_solar_panel(solar_panel_id: str):
    """
    Delete a solar panel.
    """
    deleted_solar_panel = solar_panel_service.delete_solar_panel(solar_panel_id)
    if not deleted_solar_panel:
        raise HTTPException(status_code=404, detail="Solar panel not found")
    return deleted_solar_panel
