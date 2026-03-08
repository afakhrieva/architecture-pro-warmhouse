from fastapi import APIRouter, Depends, status, HTTPException
from uuid import UUID
from typing import List
from app.schemas import Location, LocationCreate, LocationUpdate, Message
from app.deps import get_current_user_id, get_db
from app.services.location_service import LocationService
from app.services.home_service import HomeService
from app.db.memory_db import MemoryDB

router = APIRouter(prefix="/api/locations", tags=["locations"])

@router.post("", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(
        location_data: LocationCreate,
        user_id: UUID = Depends(get_current_user_id),
        db: MemoryDB = Depends(get_db)
):
    """Создать новую комнату"""
    home_service = HomeService(db)
    location_service = LocationService(db, home_service)
    return location_service.create_location(location_data, user_id)

@router.get("/home/{home_id}", response_model=List[Location])
async def get_home_locations(
        home_id: int,  # числовой ID дома
        user_id: UUID = Depends(get_current_user_id),
        db: MemoryDB = Depends(get_db)
):
    """Получить все комнаты в доме"""
    home_service = HomeService(db)
    location_service = LocationService(db, home_service)
    return location_service.get_home_locations(home_id, user_id)

@router.get("/{location_id}", response_model=Location)
async def get_location(
        location_id: int,  # числовой ID
        user_id: UUID = Depends(get_current_user_id),
        db: MemoryDB = Depends(get_db)
):
    """Получить комнату по ID"""
    home_service = HomeService(db)
    location_service = LocationService(db, home_service)
    return location_service.get_location(location_id, user_id)

@router.patch("/{location_id}", response_model=Location)
async def update_location(
        location_id: int,  # числовой ID
        location_update: LocationUpdate,
        user_id: UUID = Depends(get_current_user_id),
        db: MemoryDB = Depends(get_db)
):
    """Обновить комнату"""
    home_service = HomeService(db)
    location_service = LocationService(db, home_service)
    return location_service.update_location(location_id, location_update, user_id)

@router.delete("/{location_id}", response_model=Message)
async def delete_location(
        location_id: int,  # числовой ID
        user_id: UUID = Depends(get_current_user_id),
        db: MemoryDB = Depends(get_db)
):
    """Удалить комнату"""
    home_service = HomeService(db)
    location_service = LocationService(db, home_service)
    location_service.delete_location(location_id, user_id)
    return {"message": "Location deleted successfully"}