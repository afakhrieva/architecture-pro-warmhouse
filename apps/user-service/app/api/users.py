from fastapi import APIRouter, Depends, status
from uuid import UUID
from app.schemas import User, UserCreate, UserUpdate, Message
from app.deps import get_current_user_id, get_db
from app.services.user_service import UserService
from app.db.memory_db import MemoryDB

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: MemoryDB = Depends(get_db)
):
    """Создать профиль пользователя"""
    service = UserService(db)
    return service.create_user(user_id, user_data)

@router.get("/me", response_model=User)
async def get_current_user(
    user_id: UUID = Depends(get_current_user_id),
    db: MemoryDB = Depends(get_db)
):
    """Получить профиль текущего пользователя"""
    service = UserService(db)
    return service.get_user(user_id)

@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: UUID,
    db: MemoryDB = Depends(get_db)
):
    """Получить пользователя по ID (для внутренних вызовов)"""
    service = UserService(db)
    return service.get_user(user_id)

@router.patch("/me", response_model=User)
async def update_user(
    user_update: UserUpdate,
    user_id: UUID = Depends(get_current_user_id),
    db: MemoryDB = Depends(get_db)
):
    """Обновить профиль текущего пользователя"""
    service = UserService(db)
    return service.update_user(user_id, user_update)