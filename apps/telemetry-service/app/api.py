from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from typing import Optional, List
import logging

from app.redis.storage import TelemetryStore
from app.models import TelemetryResponse, TelemetryPoint

logger = logging.getLogger(__name__)
router = APIRouter()

async def get_store() -> TelemetryStore:
    from app.main import store
    if not store or not store.redis:
        raise HTTPException(status_code=503, detail="Storage not ready")
    return store

@router.get("/api/telemetry/{device_id}/{metric}", response_model=TelemetryResponse)
async def get_telemetry(
        device_id: str,
        metric: str,
        hours: int = Query(24, description="Сколько часов истории вернуть", ge=1, le=168),
        limit: int = Query(1000, description="Максимум точек", ge=1, le=10000),
        store: TelemetryStore = Depends(get_store)
):
    """
    Получить историю телеметрии устройства за последние N часов
    """
    try:
        # Рассчитываем временной интервал
        to_time = datetime.now().timestamp()
        from_time = (datetime.now() - timedelta(hours=hours)).timestamp()

        # Получаем данные из Redis
        points = await store.get_history(
            device_id=device_id,
            metric=metric,
            from_time=from_time,
            to_time=to_time,
            limit=limit
        )

        # Преобразуем в формат ответа
        data = [
            TelemetryPoint(time=time_iso, value=value)
            for time_iso, value in points
        ]

        return TelemetryResponse(
            device_id=device_id,
            metric=metric,
            data=data
        )

    except Exception as e:
        logger.error(f"Error getting telemetry: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/telemetry/{device_id}/latest")
async def get_latest(
        device_id: str,
        metrics: str = Query(..., description="Метрики через запятую (например: temperature,humidity)"),
        store: TelemetryStore = Depends(get_store)
):
    """
    Получить последние значения нескольких метрик
    """
    try:
        metric_list = [m.strip() for m in metrics.split(",")]

        # Получаем последние значения
        result = {}
        for metric in metric_list:
            latest = await store.get_latest(device_id, metric)
            if latest:
                time_iso, value = latest
                result[metric] = {
                    "value": value,
                    "time": time_iso
                }

        return {
            "device_id": device_id,
            "timestamp": datetime.now().isoformat(),
            "values": result
        }

    except Exception as e:
        logger.error(f"Error getting latest values: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/telemetry/{device_id}/{metric}/latest")
async def get_latest_metric(
        device_id: str,
        metric: str,
        store: TelemetryStore = Depends(get_store)
):
    """
    Получить последнее значение конкретной метрики
    """
    try:
        latest = await store.get_latest(device_id, metric)

        if latest:
            time_iso, value = latest
            return {
                "device_id": device_id,
                "metric": metric,
                "value": value,
                "time": time_iso
            }
        else:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for {device_id}:{metric}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting latest metric: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/debug")
async def debug(store: TelemetryStore = Depends(get_store)):
    """Отладочная информация"""
    return {
        "store_initialized": store is not None,
        "redis_connected": store.redis is not None
    }