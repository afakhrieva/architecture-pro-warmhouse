from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from enum import Enum

# ---------- User  ----------
class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    avatar_url: Optional[str] = None
    language: str = "ru"

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    avatar_url: Optional[str] = None
    language: Optional[str] = None

class User(UserBase):
    id: UUID  # UUID из Auth Service
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ---------- Home ----------
class HomeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    address: Optional[str] = None
    timezone: str = "Europe/Moscow"

class HomeCreate(HomeBase):
    pass

class HomeUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    timezone: Optional[str] = None

class Home(HomeBase):
    id: int  # числовой ID для URL
    uuid: UUID  # UUID для внутренних связей
    owner_id: UUID  # UUID владельца из Auth Service
    created_at: datetime
    updated_at: datetime
    member_count: Optional[int] = 0
    room_count: Optional[int] = 0

    class Config:
        from_attributes = True

# ---------- Location ----------
class LocationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    floor: Optional[int] = None

class LocationCreate(LocationBase):
    home_id: int  # числовой ID дома

class LocationUpdate(BaseModel):
    name: Optional[str] = None
    floor: Optional[int] = None

class Location(LocationBase):
    id: int  # числовой ID для URL
    uuid: UUID  # UUID для внутренних связей
    home_id: int  # числовой ID дома
    home_uuid: UUID  # UUID дома (для связей с другими сервисами)
    created_at: datetime
    updated_at: datetime
    device_count: Optional[int] = 0

    class Config:
        from_attributes = True

# ---------- Ответы ----------
class Message(BaseModel):
    message: str