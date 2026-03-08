from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Настройки приложения"""

    # Kafka
    kafka_topic: str = "device.telemetry"
    kafka_servers: str = "localhost:9092"
    kafka_group_id: str = "telemetry-service"

    # Redis
    redis_url: str = "redis://localhost:6379"
    redis_ttl_days: int = 7  # сколько дней хранить телеметрию

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8003

    class Config:
        env_file = ".env"
        case_sensitive = False

# Глобальный экземпляр настроек
settings = Settings()