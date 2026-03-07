package ru.yandex.practicum.arch.smarthome.deviceservice.external

import com.fasterxml.jackson.annotation.JsonProperty
import java.time.Instant

data class SmartHomeSensor(
    val id: String,                    // "temp-living-1"
    val name: String,                   // "Датчик в гостиной"
    val value: Double?,                  // 22.5
    val unit: String?,                   // "celsius"
    val location: String?,                // "living_room"
    val status: String,                   // "active", "inactive", "error"

    @JsonProperty("last_updated")
    val lastUpdated: Instant?              // когда последний раз обновлялось
)