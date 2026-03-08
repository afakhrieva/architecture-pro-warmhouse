package ru.yandex.practicum.arch.smarthome.deviceservice.service

import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Service
import ru.yandex.practicum.arch.smarthome.deviceservice.external.SmartHomeClient
import ru.yandex.practicum.arch.smarthome.deviceservice.external.SmartHomeSensor
import ru.yandex.practicum.arch.smarthome.deviceservice.model.Device
import ru.yandex.practicum.arch.smarthome.deviceservice.storage.InMemoryStorage

@Service
class SmartHomeAdapterService(
    private val smartHomeClient: SmartHomeClient,
    private val storage: InMemoryStorage
) {

    // Синхронизация нужна пока полностью не отключим монолит от трафика:
    // 1. Получения новых устройств, созданных через старый API
    // 2. Обновления информации об устройствах
    // 3. Поддержания актуальности данных

    // Это так себе решение, лучше читать топик событий о сенсорах из монолита и сохранять себе в бд
    @Scheduled(fixedDelay = 30000) // каждые 30 секунд для примера
    fun syncWithMonolith() {
        val monolithSensors = smartHomeClient.getAllSensors()

        monolithSensors.forEach { sensor ->
            val existingDevice = storage.findByExtId(sensor.id)

            if (existingDevice == null) {
                // Новое устройство - создаем
                createDevice(sensor)
            } else {
                // Проверяем, не изменилось ли что-то
                if (needsUpdate(sensor, existingDevice)) {
                    updateDevice(existingDevice.id, sensor)
                }
            }
        }
    }

    private fun updateDevice(id: String, sensor: SmartHomeSensor) {
        // TODO implement
    }

    private fun needsUpdate(
        sensor: SmartHomeSensor,
        existingDevice: Device
    ): Boolean {
        return existingDevice.id == sensor.id
    }

    private fun createDevice(sensor: SmartHomeSensor) {
        // TODO implement
    }
}