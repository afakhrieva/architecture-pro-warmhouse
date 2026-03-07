package ru.yandex.practicum.arch.smarthome.deviceservice.dto

import com.fasterxml.jackson.annotation.JsonProperty

data class DeviceStateResponse(
    val deviceId: String,
    val timestamp: String,
    val state: Map<String, Any>
)