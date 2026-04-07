from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional
from datetime import datetime


# ============ AUTH SCHEMAS ============

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username for the account")
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, max_length=100, description="Password (min 6 characters)")


class UserLogin(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============ TAG SCHEMAS ============

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


# ============ LINK SCHEMAS ============

class LinkCreate(BaseModel):
    url: HttpUrl = Field(..., description="URL of the link")
    title: Optional[str] = Field(None, max_length=200, description="Link title")
    description: Optional[str] = Field(None, max_length=1000, description="Link description")
    tag_ids: list[int] = Field(default=[], description="List of tag IDs to associate with this link")


class LinkUpdate(BaseModel):
    url: Optional[HttpUrl] = None
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


# ============ COMMON SCHEMAS ============

class Message(BaseModel):
    message: str
