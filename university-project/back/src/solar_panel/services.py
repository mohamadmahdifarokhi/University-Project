from typing import List, Optional
from bson import ObjectId
from ..db.db import client, db

from src.solar_panel.schemas import SolarPanelOut, SolarPanelCreate, SolarPanelUpdate


class SolarPanelService:

    def __init__(self):
        self.db = db

    def create_solar_panel(self, panel_data: SolarPanelCreate) -> SolarPanelOut:
        panel_id = ObjectId()
        panel_data_dict = panel_data.dict()
        panel_data_dict["_id"] = panel_id
        self.db.solar_panels.insert_one(panel_data_dict)
        return SolarPanelOut(id=str(panel_id), **panel_data_dict)

    def get_solar_panels(self, skip: int = 0, limit: int = 10) -> List[SolarPanelOut]:
        panels = list(self.db.solar_panels.find().skip(skip).limit(limit))
        for panel in panels:
            user = self.db.users.find_one({"_id": ObjectId(panel['user_id'])})
            print(user)
            panel["id"] = str(panel["_id"])
            panel["email"] = str(user["email"])
            panel["status"] = 'available'
        return panels

    def get_solar_panel(self, panel_id: str) -> Optional[SolarPanelOut]:
        panel = self.db.solar_panels.find_one({"_id": ObjectId(panel_id)})
        user = self.db.users.find_one({"_id": ObjectId(panel['user_id'])})
        print(user)
        panel["_id"] = str(panel["_id"])
        panel["email"] = str(user["email"])
        panel["status"] = 'available'
        if panel:
            panel["id"] = str(panel["_id"])
            return panel
        return None

    def update_solar_panel(self, panel_id: str, panel_update: SolarPanelUpdate) -> Optional[SolarPanelOut]:
        update_data = panel_update.dict(exclude_unset=True)
        result = self.db.solar_panels.update_one({"_id": ObjectId(panel_id)}, {"$set": update_data})
        if result.modified_count:
            updated_panel = self.db.solar_panels.find_one({"_id": ObjectId(panel_id)})
            updated_panel["_id"] = str(updated_panel["_id"])
            return updated_panel
        return None

    def delete_solar_panel(self, panel_id: str) -> Optional[SolarPanelOut]:
        panel = self.db.solar_panels.find_one({"_id": ObjectId(panel_id)})
        if panel:
            self.db.solar_panels.delete_one({"_id": ObjectId(panel_id)})
            panel["_id"] = str(panel["_id"])
            return panel
        return None
