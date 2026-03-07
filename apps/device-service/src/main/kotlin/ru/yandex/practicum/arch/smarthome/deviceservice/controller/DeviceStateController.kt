package ru.yandex.practicum.arch.smarthome.deviceservice.controller

import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import ru.yandex.practicum.arch.smarthome.deviceservice.dto.DeviceStateResponse
import ru.yandex.practicum.arch.smarthome.deviceservice.service.DeviceStateService

@RestController
@RequestMapping("/api/devices")
class DeviceStateController(
    private val deviceStateService: DeviceStateService
) {

    @GetMapping("/{deviceId}/state")
    fun getDeviceState(@PathVariable deviceId: String): ResponseEntity<DeviceStateResponse> {
        val state = deviceStateService.getDeviceState(deviceId)
        return if (state != null) {
            ResponseEntity.ok(state)
        } else {
            ResponseEntity.notFound().build()
        }
    }

    // Внутренний эндпоинт для MQTT listener
    @PostMapping("/{deviceId}/state")
    fun updateDeviceState(
        @PathVariable deviceId: String,
        @RequestBody state: Map<String, Any>
    ): ResponseEntity<DeviceStateResponse> {
        val updated = deviceStateService.updateDeviceState(deviceId, state)
        return if (updated != null) {
            ResponseEntity.ok(updated)
        } else {
            ResponseEntity.notFound().build()
        }
    }
}