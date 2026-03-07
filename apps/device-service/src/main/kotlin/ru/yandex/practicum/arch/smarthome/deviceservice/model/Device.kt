package ru.yandex.practicum.arch.smarthome.deviceservice.model

import java.time.Instant
import java.util.*

data class Device(
    val id: String = UUID.randomUUID().toString(),
    val name: String,
    val type: DeviceType,
    val homeId: Long,
    val roomId: Long? = null,
    val userId: String,
    val status: DeviceStatus,
    val capabilities: List<DeviceCapability> = emptyList(),
    val createdAt: Instant = Instant.now(),
    val updatedAt: Instant = Instant.now(),
    val extId: String? = null,   // id датчика в монолите
)