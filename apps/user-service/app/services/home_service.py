# app/services/home_service.py
from uuid import UUID, uuid4
from datetime import datetime
from fastapi import HTTPException
from typing import List, Optional
from app.schemas import Home, HomeCreate, HomeUpdate
from app.db.memory_db import MemoryDB

class HomeService:
    def __init__(self, db: MemoryDB):
        self.db = db

    def create_home(self, owner_id: UUID, home_data: HomeCreate) -> Home:
        """Создать новый дом"""
        home_id = self.db.next_home_id
        self.db.next_home_id += 1

        home_uuid = uuid4()
        home = Home(
            id=home_id,  # числовой ID для URL
            uuid=home_uuid,  # UUID для внутренних связей
            owner_id=owner_id,
            **home_data.dict(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self.db.add_home(home)
        return home

    def get_home(self, home_id: int, user_id: Optional[UUID] = None) -> Home:
        """Получить дом по ID """
        home = self.db.get_home(home_id)
        if not home:
            raise HTTPException(404, "Home not found")

        # Проверяем доступ, если передан user_id
        if user_id and home.owner_id != user_id:
            raise HTTPException(403, "Access denied")

        # Добавляем количество комнат
        home.room_count = len(self.db.get_locations_by_home(home_id))

        return home

    def get_user_homes(self, user_id: UUID) -> List[Home]:
        """Получить все дома пользователя"""
        user_homes = [
            home for home in self.db.homes_by_id.values()
            if home.owner_id == user_id
        ]

        # Добавляем количество комнат для каждого дома
        for home in user_homes:
            home.room_count = len(self.db.get_locations_by_home(home.id))

        return user_homes

    def update_home(self, home_id: int, user_id: UUID, home_update: HomeUpdate) -> Home:
        """Обновить дом (только владелец)"""
        home = self.get_home(home_id, user_id)  # проверяет доступ

        update_data = home_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(home, field, value)
        home.updated_at = datetime.now()

        # Обновляем в БД
        self.db.add_home(home)
        return home

    def delete_home(self, home_id: int, user_id: UUID):
        """Удалить дом (только владелец)"""
        home = self.get_home(home_id, user_id)
        if home:
            self.db.delete_home(home)

        # Отправляем событие HomeDeleted во внутреннюю шину событий
        # DeliveryService читает событие и удаляет связанные с домом устройства