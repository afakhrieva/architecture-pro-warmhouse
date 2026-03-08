package ru.yandex.practicum.arch.smarthome.deviceservice.storage

import org.springframework.stereotype.Component
import ru.yandex.practicum.arch.smarthome.deviceservice.model.Command
import ru.yandex.practicum.arch.smarthome.deviceservice.model.Device
import ru.yandex.practicum.arch.smarthome.deviceservice.model.DeviceState
import java.util.concurrent.ConcurrentHashMap

@Component
class InMemoryStorage {
    // In-memory хранилища (в реальности заменить на БД)

    final val devices = ConcurrentHashMap<String, Device>()
    final val deviceStates = ConcurrentHashMap<String, DeviceState>()
    final val commands = ConcurrentHashMap<String, Command>()

    fun findByExtId(extId: String): Device? {
        // TODO implement
        return null
    }
}