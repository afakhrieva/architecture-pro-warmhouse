package ru.yandex.practicum.arch.smarthome.deviceservice.dto

import ru.yandex.practicum.arch.smarthome.deviceservice.model.CommandType

data class CommandRequest(
    val type: CommandType,
    val params: Map<String, Any> = emptyMap()
)

data class BatchCommandRequest(
    val commands: List<BatchCommandItem>
)

data class BatchCommandItem(
    val deviceId: String,
    val type: CommandType,
    val params: Map<String, Any> = emptyMap()
)