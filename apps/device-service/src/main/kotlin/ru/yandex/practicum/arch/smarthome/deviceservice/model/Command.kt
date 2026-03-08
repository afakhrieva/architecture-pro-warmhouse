package ru.yandex.practicum.arch.smarthome.deviceservice.model

import java.time.Instant
import java.util.UUID

data class Command(
    val id: String = UUID.randomUUID().toString(),
    val deviceId: String,
    val type: CommandType,
    val params: Map<String, Any> = emptyMap(),
    val status: CommandStatus = CommandStatus.PENDING,
    val createdAt: Instant = Instant.now(),
    val executedAt: Instant? = null,
    val error: String? = null
)
