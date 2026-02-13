from datetime import datetime
from pydantic import BaseModel, EmailStr

from ..models import Role


class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: Role
    tenant_id: int
    created_at: datetime

    class Config:
        from_attributes = True
