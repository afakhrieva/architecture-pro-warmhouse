from uuid import UUID
from datetime import datetime
from fastapi import HTTPException
from app.schemas import User, UserCreate, UserUpdate
from app.db.memory_db import MemoryDB

class UserService:
    def __init__(self, db: MemoryDB):
        self.db = db

    def create_user(self, user_id: UUID, user_data: UserCreate) -> User:
        """Создать нового пользователя"""
        if user_id in self.db.users:
            raise HTTPException(400, "User profile already exists")

        user = User(
            id=user_id,
            **user_data.dict(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.db.users[user_id] = user
        return user

    def get_user(self, user_id: UUID) -> User:
        """Получить пользователя по ID"""
        user = self.db.users.get(user_id)
        if not user:
            raise HTTPException(404, "User not found")
        return user

    def update_user(self, user_id: UUID, user_update: UserUpdate) -> User:
        """Обновить пользователя"""
        user = self.get_user(user_id)

        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        user.updated_at = datetime.now()

        self.db.users[user_id] = user
        return user