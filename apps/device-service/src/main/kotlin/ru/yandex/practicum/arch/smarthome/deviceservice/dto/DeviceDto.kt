package ru.yandex.practicum.arch.smarthome.deviceservice.dto

import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.NotNull
import ru.yandex.practicum.arch.smarthome.deviceservice.model.CommandStatus
import ru.yandex.practicum.arch.smarthome.deviceservice.model.CommandType
import ru.yandex.practicum.arch.smarthome.deviceservice.model.DeviceCapability
import ru.yandex.practicum.arch.smarthome.deviceservice.model.DeviceStatus
import ru.yandex.practicum.arch.smarthome.deviceservice.model.DeviceType

data class CreateDeviceRequest(
    @field:NotBlank
    val name: String,

    @field:NotNull
    val type: DeviceType,

    @field:NotNull
    val homeId: Long,

    val locationId: Long? = null,

    val capabilities: List<DeviceCapability> = emptyList()
)

data class UpdateDeviceRequest(
    val name: String? = null,
    val locationId: Long? = null
)

data class DeviceResponse(
    val id: String,
    val name: String,
    val type: DeviceType,
    val homeId: Long,
    val locationId: Long?,
    val userId: String,
    val status: DeviceStatus,
    val capabilities: List<DeviceCapability>,
    val createdAt: String,
    val updatedAt: String
)

data class CommandResponse(
    val commandId: String,
    val deviceId: String,
    val type: CommandType,
    val status: CommandStatus,
    val createdAt: String
)

data class ErrorResponse(
    val code: Int,
    val message: String
)