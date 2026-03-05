from uuid import UUID
from typing import Optional
from app.models import Device
from app.repositories import DeviceRepository

class DeviceService:
    def __init__(self, repo: DeviceRepository):
        self.repo = repo

    async def get_by_ext_id(self, ext_id: str) -> Optional[Device]:
        """
        Получить устройство по внешнему ID (MAC, серийный номер)
        """
        return await self.repo.find_by_ext_id(ext_id)

    async def get_by_id(self, device_id: UUID) -> Optional[Device]:
        """Получить устройство по внутреннему UUID"""
        return await self.repo.find_by_id(device_id)