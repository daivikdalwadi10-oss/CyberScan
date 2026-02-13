from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import AssetType, AssetHealth

class AssetBase(BaseModel):
    name: str
    type: AssetType
    health: AssetHealth = AssetHealth.HEALTHY
    uptime_percentage: float = 100.0
    risk_level: str = "Low"
    owner_id: Optional[str] = None
    last_incident_id: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    health: Optional[AssetHealth] = None
    risk_level: Optional[str] = None
    owner_id: Optional[str] = None
    last_incident_id: Optional[str] = None

class AssetOut(AssetBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
