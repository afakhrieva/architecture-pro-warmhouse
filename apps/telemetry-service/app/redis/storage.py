import redis.asyncio as redis
from datetime import datetime
from typing import List, Optional, Tuple
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class TelemetryStore:
    """
    Хранит телеметрию в Redis sorted sets
    Ключ: "telemetry:{device_id}:{metric}"
    Score: timestamp (float)
    Member: value (str)
    """

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis = None
        self.ttl_seconds = settings.redis_ttl_days * 24 * 60 * 60

    async def connect(self):
        """Подключение к Redis"""
        self.redis = await redis.from_url(
            self.redis_url,
            decode_responses=True
        )
        logger.info("Connected to Redis")

    async def close(self):
        """Закрытие соединения"""
        if self.redis:
            await self.redis.close()
            logger.info("Redis connection closed")

    async def save(self, device_id: str, metric: str, timestamp: float, value: float):
        """
        Сохранить одну точку телеметрии
        """
        key = f"telemetry:{device_id}:{metric}"

        # Используем значение + timestamp как уникальный member
        member = f"{value}:{timestamp}"

        await self.redis.zadd(key, {member: timestamp})
        await self.redis.expire(key, self.ttl_seconds)

        logger.debug(f" Saved {device_id}:{metric} = {value} at {timestamp}")

    async def save_batch(self, points: List[Tuple[str, str, float, float]]):
        """
        Сохранить пачку точек
        points: list of (device_id, metric, timestamp, value)
        """
        if not points:
            return

        pipeline = self.redis.pipeline()

        for device_id, metric, timestamp, value in points:
            key = f"telemetry:{device_id}:{metric}"
            member = f"{value}:{timestamp}"

            pipeline.zadd(key, {member: timestamp})
            pipeline.expire(key, self.ttl_seconds)

        await pipeline.execute()
        logger.debug(f" Saved batch of {len(points)} points")

    async def get_history(self, device_id: str, metric: str,
                          from_time: float, to_time: float,
                          limit: int = 1000) -> List[Tuple[str, float]]:
        """
        Получить историю значений
        """
        key = f"telemetry:{device_id}:{metric}"

        points = await self.redis.zrange(
            key,
            from_time,
            to_time,
            byscore=True,
            withscores=True,
            offset=0,
            num=limit
        )


        result = []
        for member, ts in points:
            # Извлекаем значение из member (формат "value:timestamp")
            value_str = member.split(':')[0]
            time_iso = datetime.fromtimestamp(ts).isoformat()
            result.append((time_iso, float(value_str)))

        return result

    async def get_latest(self, device_id: str, metric: str) -> Optional[Tuple[str, float]]:
        """
        Получить последнее значение метрики
        """
        key = f"telemetry:{device_id}:{metric}"

        # Получаем последние 10 записей (на случай одинаковых значений)
        all_values = await self.redis.zrevrange(key, 0, 9, withscores=True)

        if all_values:
            # Берём самую последнюю по времени
            latest = max(all_values, key=lambda x: x[1])
            member, ts = latest
            value_str = member.split(':')[0]
            return (datetime.fromtimestamp(ts).isoformat(), float(value_str))
        return None

    async def get_latest_batch(self, device_id: str, metrics: List[str]) -> dict:
        """
        Получить последние значения для нескольких метрик
        """
        pipeline = self.redis.pipeline()

        for metric in metrics:
            key = f"telemetry:{device_id}:{metric}"
            pipeline.zrevrange(key, 0, 9, withscores=True)  # берем последние 10

        results = await pipeline.execute()

        latest = {}
        for metric, result in zip(metrics, results):
            if result:
                # Находим самую последнюю по времени
                latest_entry = max(result, key=lambda x: x[1])
                member, ts = latest_entry
                value_str = member.split(':')[0]
                latest[metric] = {
                    "value": float(value_str),
                    "time": datetime.fromtimestamp(ts).isoformat()
                }

        return latest