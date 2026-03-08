package ru.yandex.practicum.arch.smarthome.deviceservice.service

import org.springframework.stereotype.Service
import ru.yandex.practicum.arch.smarthome.deviceservice.dto.BatchCommandRequest
import ru.yandex.practicum.arch.smarthome.deviceservice.dto.CommandRequest
import ru.yandex.practicum.arch.smarthome.deviceservice.dto.CommandResponse
import ru.yandex.practicum.arch.smarthome.deviceservice.model.Command
import ru.yandex.practicum.arch.smarthome.deviceservice.model.CommandStatus
import ru.yandex.practicum.arch.smarthome.deviceservice.model.CommandType
import ru.yandex.practicum.arch.smarthome.deviceservice.storage.InMemoryStorage
import java.time.Instant
import kotlin.collections.set

@Service
class CommandService(
    private val storage: InMemoryStorage,
    private val deviceStateService: DeviceStateService
) {

    private val devices = storage.devices
    private val commands = storage.commands

    companion object {
        private const val DEFAULT_POWER_STATE = "off"
        private const val DEFAULT_TARGET_TEMPERATURE = 22
    }

    fun sendCommand(deviceId: String, request: CommandRequest): CommandResponse? {
        val device = devices[deviceId] ?: return null

        // Проверяем, поддерживает ли устройство такую команду
        // В реальности проверять по capabilities

        val command = Command(
            deviceId = deviceId,
            type = request.type,
            params = request.params
        )

        commands[command.id] = command

        // Имитируем отправку команды
        processCommand(command)

        return CommandResponse(
            commandId = command.id,
            deviceId = command.deviceId,
            type = command.type,
            status = command.status,
            createdAt = DATE_FORMATTER.format(command.createdAt)
        )
    }

    fun sendBatchCommands(request: BatchCommandRequest): List<CommandResponse> {
        return request.commands.mapNotNull { item ->
            sendCommand(item.deviceId, CommandRequest(item.type, item.params))
        }
    }

    fun getCommand(commandId: String): Command? {
        return commands[commandId]
    }

    // Имитация обработки команды
    private fun processCommand(command: Command) {

        // В реальности здесь отправка команд в MQTT или по HTTP в бывший монолит для команд для старых термостатов
        // По задаче там предполагается управление отоплением

        // Обновляем статус команды
        val updatedCommand = command.copy(
            status = CommandStatus.SENT,
            executedAt = Instant.now()
        )
        commands[command.id] = updatedCommand

        // Для некоторых команд обновляем состояние устройства
        when (command.type) {
            CommandType.SET_POWER -> {
                val powerState = mapOf("power" to (command.params["state"] ?: DEFAULT_POWER_STATE))
                deviceStateService.updateDeviceState(command.deviceId, powerState)
            }
            CommandType.SET_TEMPERATURE -> {
                val tempState = mapOf("target_temperature" to (command.params["temperature"]
                    ?: DEFAULT_TARGET_TEMPERATURE))
                deviceStateService.updateDeviceState(command.deviceId, tempState)
            }
            else -> {}
        }
    }
}