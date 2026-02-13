from datetime import datetime
from pydantic import BaseModel, Field


class TenantCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)


class TenantRead(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
