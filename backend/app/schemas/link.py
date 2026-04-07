from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime

from app.schemas.tag import TagResponse


class LinkCreate(BaseModel):
    url: HttpUrl = Field(..., description="URL of the link")
    title: Optional[str] = Field(None, max_length=200, description="Link title")
    description: Optional[str] = Field(None, max_length=1000, description="Link description")
    tag_ids: list[int] = Field(default=[], description="List of tag IDs to associate with this link")


class LinkUpdate(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    tag_ids: Optional[list[int]] = None


class LinkResponse(BaseModel):
    id: int
    url: str
    title: Optional[str]
    description: Optional[str]
    user_id: int
    tags: list[TagResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LinkList(BaseModel):
    links: list[LinkResponse]
    total: int
