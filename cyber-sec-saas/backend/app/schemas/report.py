from datetime import datetime
from pydantic import BaseModel


class ReportResponse(BaseModel):
    scan_id: int
    generated_at: datetime
    risk_score: int
