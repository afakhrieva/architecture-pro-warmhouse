from fastapi import APIRouter, Depends, status, HTTPException
from uuid import UUID
from typing import List
from app.schemas import Home, HomeCreate, HomeUpdate, Message
from app.deps import get_current_user_id, get_db
from app.services.home_service import HomeService
from app.services.location_service import LocationService
from app.db.memory_db import MemoryDB

router = APIRouter(prefix="/api/homes", tags=["homes"])

@router.post("", response_model=Home, status_code=status.HTTP_201_CREATED)
async def create_home(
        home_data: HomeCreate,
        user_id: UUID = Depends(get_current_user_id),
        db: MemoryDB = Depends(get_db)
):
    """Создать новый дом"""
    service = HomeService(db)
    return service.create_home(user_id, home_data)

@router.get("", response_model=List[Home])
async def get_my_homes(
        user_id: UUID = Depends(get_current_user_id),
        db: MemoryDB = Depends(get_db)
):
    """Получить все дома текущего пользователя"""
    service = HomeService(db)
    return service.get_user_homes(user_id)

@router.get("/{home_id}", response_model=Home)
async def get_home(
        home_id: int,  # числовой ID в URL
        user_id: UUID = Depends(get_current_user_id),
        db: MemoryDB = Depends(get_db)
):
    """Получить дом по ID"""
    service = HomeService(db)
    return service.get_home(home_id, user_id)

@router.patch("/{home_id}", response_model=Home)
async def update_home(
        home_id: int,  # числовой ID
        home_update: HomeUpdate,
        user_id: UUID = Depends(get_current_user_id),
        db: MemoryDB = Depends(get_db)
):
    """Обновить дом"""
    service = HomeService(db)
    return service.update_home(home_id, user_id, home_update)

@router.delete("/{home_id}", response_model=Message)
async def delete_home(
        home_id: int,  # числовой ID
        user_id: UUID = Depends(get_current_user_id),
        db: MemoryDB = Depends(get_db)
):
    """Удалить дом"""
    service = HomeService(db)
    service.delete_home(home_id, user_id)
    return {"message": "Home deleted successfully"}