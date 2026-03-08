import aiokafka
import json
import asyncio
from datetime import datetime
from typing import Optional
import logging
from app.config import settings
from app.redis.storage import TelemetryStore
from app.models import RawTelemetryMessage

logger = logging.getLogger(__name__)

class TelemetryConsumer:
    """Читает телеметрию из Kafka и сохраняет в Redis"""

    def __init__(self, store: TelemetryStore):
        self.store = store
        self.consumer: Optional[aiokafka.AIOKafkaConsumer] = None
        self.running = False

    async def start(self):
        """Запуск consumer'а"""
        self.consumer = aiokafka.AIOKafkaConsumer(
            settings.kafka_topic,
            bootstrap_servers=settings.kafka_servers,
            group_id=settings.kafka_group_id,
            value_deserializer=lambda m: json.loads(m.decode()),
            auto_offset_reset="earliest",
            enable_auto_commit=True
        )

        await self.consumer.start()
        self.running = True
        logger.info(f"Kafka consumer started, listening to {settings.kafka_topic}")

        # Запускаем бесконечный цикл обработки
        asyncio.create_task(self._consume_loop())

    async def stop(self):
        """Остановка consumer'а"""
        self.running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info("Kafka consumer stopped")

    async def _consume_loop(self):
        """Основной цикл обработки сообщений"""
        try:
            async for msg in self.consumer:
                if not self.running:
                    break

                await self._process_message(msg.value)

        except Exception as e:
            logger.error(f"Consumer error: {e}")
        finally:
            await self.stop()

    async def _process_message(self, raw_data: dict):
        """
        Обработать одно сообщение из Kafka
        """
        try:
            # Валидируем сообщение
            msg = RawTelemetryMessage(**raw_data)

            device_id = msg.device_id

            # Парсим timestamp
            if msg.timestamp:
                dt = datetime.fromisoformat(msg.timestamp.replace('Z', '+00:00'))
                ts = dt.timestamp()
            else:
                ts = datetime.now().timestamp()

            # Собираем все точки для batch-сохранения
            points = []

            # Рекурсивно обходим payload в поисках чисел
            self._extract_metrics(device_id, "", msg.payload, ts, points)

            # Сохраняем батчем
            if points:
                await self.store.save_batch(points)
                logger.debug(f"Processed {len(points)} metrics from {device_id}")

        except Exception as e:
            logger.error(f"Failed to process message: {e}")

    def _extract_metrics(self, device_id: str, prefix: str,
                         obj: any, timestamp: float,
                         points: list):
        """
        Рекурсивно извлекает все числовые значения из объекта
        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{prefix}.{key}" if prefix else key
                self._extract_metrics(device_id, full_key, value, timestamp, points)

        elif isinstance(obj, (int, float)):
            points.append((device_id, prefix, timestamp, float(obj)))

        elif isinstance(obj, list):
            for i, value in enumerate(obj):
                self._extract_metrics(device_id, f"{prefix}[{i}]", value, timestamp, points)