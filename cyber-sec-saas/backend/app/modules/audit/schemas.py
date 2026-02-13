from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any
from .models import AuditAction

class AuditLogBase(BaseModel):
    user_id: Optional[str] = None
    action: AuditAction
    details: Optional[Any] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogOut(AuditLogBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True
