package ru.yandex.practicum.arch.smarthome.deviceservice.service

import org.springframework.stereotype.Service
import ru.yandex.practicum.arch.smarthome.deviceservice.dto.DeviceStateResponse
import ru.yandex.practicum.arch.smarthome.deviceservice.model.DeviceStatus
import ru.yandex.practicum.arch.smarthome.deviceservice.storage.InMemoryStorage
import java.time.Instant
import kotlin.collections.plus

@Service
class DeviceStateService(
    private val storage: InMemoryStorage
) {
    private val devices = storage.devices
    private val deviceStates = storage.deviceStates

    fun getDeviceState(deviceId: String): DeviceStateResponse? {
        val state = deviceStates[deviceId] ?: return null
        return DeviceStateResponse(
            deviceId = state.deviceId,
            timestamp = DATE_FORMATTER.format(state.timestamp),
            state = state.state
        )
    }

    fun updateDeviceState(deviceId: String, newState: Map<String, Any>): DeviceStateResponse? {
        val currentState = deviceStates[deviceId] ?: return null

        val updatedState = currentState.copy(
            timestamp = Instant.now(),
            state = currentState.state + newState
        )

        deviceStates[deviceId] = updatedState

        // Обновляем статус устройства
        if (newState.containsKey("online")) {
            devices[deviceId]?.let { device ->
                val updatedDevice = device.copy(
                    status = if (newState["online"] == true) DeviceStatus.ONLINE else DeviceStatus.OFFLINE,
                    updatedAt = Instant.now()
                )
                devices[deviceId] = updatedDevice
            }
        }

        return DeviceStateResponse(
            deviceId = updatedState.deviceId,
            timestamp = DATE_FORMATTER.format(updatedState.timestamp),
            state = updatedState.state
        )
    }
}