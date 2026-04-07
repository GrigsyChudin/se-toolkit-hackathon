from pydantic import BaseModel, Field
from datetime import datetime


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Tag name")
    color: str = Field("#3B82F6", pattern=r"^#[0-9A-Fa-f]{6}$", description="Hex color code")


class TagResponse(BaseModel):
    id: int
    name: str
    color: str
    created_at: datetime

    class Config:
        from_attributes = True


class TagList(BaseModel):
    tags: list[TagResponse]
    total: int
