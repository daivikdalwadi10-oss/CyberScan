from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .models import IncidentStatus

class IncidentBase(BaseModel):
    title: str
    description: Optional[str] = None

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    status: Optional[IncidentStatus] = None
    assigned_to_id: Optional[int] = None
    description: Optional[str] = None
    timeline: Optional[str] = None
    evidence: Optional[str] = None

class IncidentOut(IncidentBase):
    id: int
    status: IncidentStatus
    created_at: datetime
    updated_at: datetime
    assigned_to_id: Optional[int]
    timeline: Optional[str]
    evidence: Optional[str]

    class Config:
        orm_mode = True
