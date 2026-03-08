package ru.yandex.practicum.arch.smarthome.deviceservice.dto

data class DeviceStateResponse(
    val deviceId: String,
    val timestamp: String,
    val state: Map<String, Any>
)