from datetime import datetime
from pydantic import BaseModel

from ..models import ScanStatus, Severity


class VulnerabilityRead(BaseModel):
    id: int
    name: str
    severity: Severity
    description: str
    recommendation: str

    class Config:
        from_attributes = True


class ScanRead(BaseModel):
    id: int
    project_id: int
    tenant_id: int
    status: ScanStatus
    risk_score: int
    started_at: datetime | None
    completed_at: datetime | None

    class Config:
        from_attributes = True


class ScanDetail(ScanRead):
    vulnerabilities: list[VulnerabilityRead]
