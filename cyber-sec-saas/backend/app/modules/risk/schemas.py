from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import ThreatLevel

class RiskScoreBase(BaseModel):
    overall_score: float
    threat_level: ThreatLevel
    critical_cve_count: int = 0
    active_alert_count: int = 0
    cloud_incident_count: int = 0
    infrastructure_load_avg: float = 0.0
    uptime_percentage: float = 100.0

class RiskScoreCreate(RiskScoreBase):
    pass

class RiskScoreOut(RiskScoreBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True
