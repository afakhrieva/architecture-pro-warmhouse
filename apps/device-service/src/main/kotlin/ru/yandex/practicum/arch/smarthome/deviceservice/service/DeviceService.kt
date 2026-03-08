package ru.yandex.practicum.arch.smarthome.deviceservice.service

import ru.yandex.practicum.arch.smarthome.deviceservice.dto.*
import ru.yandex.practicum.arch.smarthome.deviceservice.model.*
import org.springframework.stereotype.Service
import ru.yandex.practicum.arch.smarthome.deviceservice.storage.InMemoryStorage
import java.time.Instant

@Service
class DeviceService(
    private val storage: InMemoryStorage
) {
    private val devices = storage.devices
    private val deviceStates = storage.deviceStates

    // ---------- BASIC CRUD ----------

    fun createDevice(request: CreateDeviceRequest, userId: String): DeviceResponse {
        val device = Device(
            name = request.name,
            type = request.type,
            homeId = request.homeId,
            locationId = request.locationId,
            userId = userId,
            status = DeviceStatus.OFFLINE,
            capabilities = request.capabilities
        )

        devices[device.id] = device

        // Инициализируем состояние
        deviceStates[device.id] = DeviceState(
            deviceId = device.id,
            state = mapOf("status" to "offline")
        )

        // Отправляем событие DeviceCreated в device.events

        return toResponse(device)
    }

    fun getDevice(deviceId: String): DeviceResponse? {
        return devices[deviceId]?.let { toResponse(it) }
    }

    fun getAllDevices(homeId: Long?, locationId: Long?, type: DeviceType?): List<DeviceResponse> {
        return devices.values
            .filter { homeId == null || it.homeId == homeId }
            .filter { locationId == null || it.locationId == locationId }
            .filter { type == null || it.type == type }
            .map { toResponse(it) }
    }

    fun updateDevice(deviceId: String, request: UpdateDeviceRequest): DeviceResponse? {
        val device = devices[deviceId] ?: return null

        val updatedDevice = device.copy(
            name = request.name ?: device.name,
            locationId = request.locationId ?: device.locationId,
            updatedAt = Instant.now()
        )

        devices[deviceId] = updatedDevice

        // Отправляем событие DeviceUpdated в device.events

        return toResponse(updatedDevice)
    }

    fun deleteDevice(deviceId: String): Boolean {
        devices.remove(deviceId)
        deviceStates.remove(deviceId)

        // Удаляем команды

        // Отправляем событие DeviceDeleted в device.events
        return true
    }

    private fun toResponse(device: Device): DeviceResponse {
        return DeviceResponse(
            id = device.id,
            name = device.name,
            type = device.type,
            homeId = device.homeId,
            locationId = device.locationId,
            userId = device.userId,
            status = device.status,
            capabilities = device.capabilities,
            createdAt = DATE_FORMATTER.format(device.createdAt),
            updatedAt = DATE_FORMATTER.format(device.updatedAt)
        )
    }
}