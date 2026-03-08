from fastapi import FastAPI
import logging
import asyncio

from app.config import settings
from app.redis.storage import TelemetryStore
from app.kafka.consumer import TelemetryConsumer
from app.api import router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

store = TelemetryStore(settings.redis_url)
consumer = TelemetryConsumer(store)

app = FastAPI(title="Telemetry Service")

app.include_router(router)

@app.on_event("startup")
async def startup():
    logger.info("Starting Telemetry Service...")

    # Подключаемся к Redis
    await store.connect()
    logger.info("Redis connected")

    # Запускаем Kafka consumer в фоне
    asyncio.create_task(consumer.start())
    logger.info("Kafka consumer starting...")

    logger.info("Telemetry Service started")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down Telemetry Service...")
    await consumer.stop()
    await store.close()
    logger.info("Telemetry Service stopped")

@app.get("/")
async def root():
    return {
        "service": "Telemetry Service",
        "status": "running",
        "docs": "/docs"
    }

__all__ = ['store']