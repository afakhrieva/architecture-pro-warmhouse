from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any, Optional

class TelemetryPoint(BaseModel):
    """Одна точка телеметрии для ответа"""
    time: str
    value: float

class TelemetryResponse(BaseModel):
    """Ответ с историей телеметрии"""
    device_id: str
    metric: str
    data: List[TelemetryPoint]

class LatestValueResponse(BaseModel):
    """Последнее значение метрики"""
    value: float
    time: str

class LatestMetricsResponse(BaseModel):
    """Ответ с последними значениями нескольких метрик"""
    device_id: str
    timestamp: str
    values: Dict[str, LatestValueResponse]

class RawTelemetryMessage(BaseModel):
    """Сырое сообщение из Kafka"""
    device_id: str
    timestamp: Optional[str] = None
    payload: Dict[str, Any]

    class Config:
        extra = "allow"  # разрешаем дополнительные поля

class HealthResponse(BaseModel):
    """Ответ на проверку здоровья"""
    status: str
    service: str