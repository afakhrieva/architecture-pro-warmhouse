# app/mqtt/listener.py
import json
import asyncio
from datetime import datetime
import paho.mqtt.client as mqtt
from app.kafka.producer import KafkaProducer
from app.services.device_service import DeviceService
from app.services.state_service import StateService
import logging

logger = logging.getLogger(__name__)

class MQTTListener:
    """
    Единственный класс, который читает MQTT топики
    """
    def __init__(self, device_service: DeviceService, state_service: StateService, kafka_producer: KafkaProducer):
        self.device_service = device_service
        self.state_service = state_service
        self.kafka_producer = kafka_producer
        self.client = mqtt.Client()

        # Настройка callback'ов
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        """Подключение к MQTT - подписываемся на всё"""
        logger.info(f"Connected to MQTT with result code {rc}")

        # Подписываемся на все топики устройств
        client.subscribe("devices/+/telemetry")  # телеметрия
        client.subscribe("devices/+/state")      # изменения состояния
        client.subscribe("devices/+/status")     # статус online/offline

    def on_message(self, client, userdata, msg):
        """Пришло сообщение от устройства"""
        try:
            # Парсим топик: devices/{device_id}/{type}

            # Парсим payload
            # device_ext_id - внешний ID устройства

            # Отправляем в асинхронную обработку
            asyncio.create_task(
                #    self.process_message(device_ext_id, msg_type, payload)
            )

        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}")

    async def process_message(self, device_ext_id: str, msg_type: str, payload: dict):
        """
        Обработка сообщения - единственное место, где данные обогащаются
        """
        # 1. Получаем внутренний ID устройства по внешнему ID

        # 2. Обогащаем данные

        # 3. Обновляем состояние в Redis

        # 4. Публикуем обогащённое событие в Kafka
        await self.kafka_producer.publish(
            topic="device.events",
            key=str(device.id),
            value=enriched_data
        )

        logger.debug(f"Processed message from {device_ext_id} -> device.events")