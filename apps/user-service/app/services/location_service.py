# app/services/location_service.py
from uuid import UUID, uuid4
from datetime import datetime
from fastapi import HTTPException
from typing import List, Optional
from app.schemas import Location, LocationCreate, LocationUpdate
from app.db.memory_db import MemoryDB
from app.services.home_service import HomeService

class LocationService:
    def __init__(self, db: MemoryDB, home_service: HomeService):
        self.db = db
        self.home_service = home_service

    def create_location(self, location_data: LocationCreate, user_id: UUID) -> Location:
        """Создать новую комнату"""
        # Проверяем, что дом существует и пользователь имеет доступ
        home = self.home_service.get_home(location_data.home_id, user_id)

        location_id = self.db.next_location_id
        self.db.next_location_id += 1

        location_uuid = uuid4()
        location = Location(
            id=location_id,  # числовой ID для URL
            uuid=location_uuid,  # UUID для внутренних связей
            home_id=location_data.home_id,  # числовой ID дома
            home_uuid=home.uuid,  # UUID дома
            **location_data.dict(exclude={'home_id'}),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self.db.add_location(location)
        return location

    def get_location(self, location_id: int, user_id: Optional[UUID] = None) -> Location:
        """Получить комнату по ID"""
        location = self.db.get_location(location_id)
        if not location:
            raise HTTPException(404, "Location not found")

        # Проверяем доступ через дом, если передан user_id
        if user_id:
            self.home_service.get_home(location.home_id, user_id)

        return location

    def get_home_locations(self, home_id: int, user_id: Optional[UUID] = None) -> List[Location]:
        """Получить все комнаты в доме"""
        # Проверяем доступ к дому
        if user_id:
            self.home_service.get_home(home_id, user_id)

        locations = self.db.get_locations_by_home(home_id)

        # Сортируем по этажу и имени
        locations.sort(key=lambda x: (x.floor or 0, x.name))

        return locations

    def update_location(self, location_id: int, location_update: LocationUpdate, user_id: UUID) -> Location:
        """Обновить комнату"""
        location = self.get_location(location_id, user_id)

        update_data = location_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(location, field, value)
        location.updated_at = datetime.now()

        # Обновляем в БД
        self.db.add_location(location)
        return location

    def delete_location(self, location_id: int, user_id: UUID):
        """Удалить комнату"""
        location = self.get_location(location_id, user_id)
        if location:
            self.db.delete_location(location)
            # Отправляем событие LocationDeleted в шину событий
            # DeviceService, прочитав такое событие, удаляет устройства привязанные к этому помещению
