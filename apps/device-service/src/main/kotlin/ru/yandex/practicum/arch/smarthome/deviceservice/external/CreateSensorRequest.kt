package ru.yandex.practicum.arch.smarthome.deviceservice.external

import com.fasterxml.jackson.annotation.JsonProperty

data class CreateSensorRequest(
    val name: String,
    val location: String? = null,
    val unit: String = "celsius",

    @JsonProperty("sensor_type")
    val sensorType: String = "temperature"
)