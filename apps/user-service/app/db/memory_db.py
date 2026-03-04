from uuid import UUID, uuid4
from typing import Dict, Optional
from app.schemas import User, Home, Location

class MemoryDB:
    def __init__(self):
        # Users
        self.users: Dict[UUID, User] = {}

        # Homes - 2 индекса
        self.homes_by_id: Dict[int, Home] = {}      # числовой ID -> Home
        self.homes_by_uuid: Dict[UUID, int] = {}    # UUID -> числовой ID

        # Locations - 3 индекса
        self.locations_by_id: Dict[int, Location] = {}    # числовой ID -> Location
        self.locations_by_uuid: Dict[UUID, int] = {}      # UUID -> числовой ID
        self.locations_by_home: Dict[int, List[int]] = {} # home_id -> list of location_ids

        # Счётчики для генерации числовых ID
        self.next_home_id = 1
        self.next_location_id = 1

    def add_home(self, home: Home) -> None:
        """Добавить дом в оба индекса"""
        self.homes_by_id[home.id] = home
        self.homes_by_uuid[home.uuid] = home.id

    def get_home(self, home_id: int) -> Optional[Home]:
        """Получить дом по числовому ID"""
        return self.homes_by_id.get(home_id)

    def delete_home(self, home: Home) -> None:
        # Удаляем все комнаты в доме
        locations = self.get_locations_by_home(home.id)
        for location in locations:
            del self.locations_by_id[location.id]
            del self.locations_by_uuid[location.uuid]
        if locations:
            del self.locations_by_home[home.id]

        # Удаляем дом
        del self.homes_by_id[home.id]
        del self.homes_by_uuid[home.uuid]

    def add_location(self, location: Location) -> None:
        """Добавить комнату в индексы"""
        self.locations_by_id[location.id] = location
        self.locations_by_uuid[location.uuid] = location.id

        # Добавляем в список комнат дома
        if location.home_id not in self.locations_by_home:
            self.locations_by_home[location.home_id] = []
        self.locations_by_home[location.home_id].append(location.id)

    def get_location(self, location_id: int) -> Optional[Location]:
        """Получить комнату по числовому ID"""
        return self.locations_by_id.get(location_id)

    def get_locations_by_home(self, home_id: int) -> list[Location]:
        """Получить все комнаты дома"""
        location_ids = self.locations_by_home.get(home_id, [])
        return [self.locations_by_id[loc_id] for loc_id in location_ids]

    def delete_location(self, location: Location)-> None:
        """Удалить комнату"""
        del self.locations_by_id[location.id]
        del self.locations_by_uuid[location.uuid]

        # Удаляем из списка комнат дома
        if location.home_id in self.locations_by_home:
            self.locations_by_home[location.home_id].remove(location.id)


db = MemoryDB()