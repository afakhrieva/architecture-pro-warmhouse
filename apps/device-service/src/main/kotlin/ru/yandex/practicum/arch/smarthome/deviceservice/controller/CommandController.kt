package ru.yandex.practicum.arch.smarthome.deviceservice.controller

import jakarta.validation.Valid
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import ru.yandex.practicum.arch.smarthome.deviceservice.dto.BatchCommandRequest
import ru.yandex.practicum.arch.smarthome.deviceservice.dto.CommandRequest
import ru.yandex.practicum.arch.smarthome.deviceservice.dto.CommandResponse
import ru.yandex.practicum.arch.smarthome.deviceservice.model.Command
import ru.yandex.practicum.arch.smarthome.deviceservice.service.CommandService

@RestController
@RequestMapping("/api/devices")
class CommandController(
    private val commandService: CommandService,
) {

    @PostMapping("/{deviceId}/commands")
    fun sendCommand(
        @PathVariable deviceId: String,
        @Valid @RequestBody request: CommandRequest
    ): ResponseEntity<CommandResponse> {
        val response = commandService.sendCommand(deviceId, request)
        return if (response != null) {
            ResponseEntity.accepted().body(response)
        } else {
            ResponseEntity.notFound().build()
        }
    }

    @PostMapping("/commands/batch")
    fun sendBatchCommands(@Valid @RequestBody request: BatchCommandRequest): List<CommandResponse> {
        return commandService.sendBatchCommands(request)
    }

    @GetMapping("/commands/{commandId}")
    fun getCommand(@PathVariable commandId: String): ResponseEntity<Command> {
        val command = commandService.getCommand(commandId)
        return if (command != null) {
            ResponseEntity.ok(command)
        } else {
            ResponseEntity.notFound().build()
        }
    }
}