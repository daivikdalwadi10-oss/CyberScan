from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    target_url: str = Field(min_length=8, max_length=2048)


class ProjectRead(BaseModel):
    id: int
    name: str
    target_url: str
    tenant_id: int

    class Config:
        from_attributes = True
