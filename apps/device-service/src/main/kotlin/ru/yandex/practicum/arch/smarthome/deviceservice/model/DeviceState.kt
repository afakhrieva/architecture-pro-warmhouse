package ru.yandex.practicum.arch.smarthome.deviceservice.model

import java.time.Instant

data class DeviceState(
    val deviceId: String,
    val timestamp: Instant = Instant.now(),
    val state: Map<String, Any> = emptyMap() // например: {"power": "on", "brightness": 50}
)