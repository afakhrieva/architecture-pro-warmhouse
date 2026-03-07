package ru.yandex.practicum.arch.smarthome.deviceservice.controller

import ru.yandex.practicum.arch.smarthome.deviceservice.dto.*
import ru.yandex.practicum.arch.smarthome.deviceservice.service.DeviceService
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import jakarta.validation.Valid
import ru.yandex.practicum.arch.smarthome.deviceservice.model.DeviceType

@RestController
@RequestMapping("/api/devices")
class DeviceController(
    private val deviceService: DeviceService
) {
    // ---------- BASIC CRUD ----------

    @PostMapping
    fun createDevice(@Valid @RequestBody request: CreateDeviceRequest): ResponseEntity<DeviceResponse> {
        val userId = getCurrentUserId()
        val device = deviceService.createDevice(request, userId)
        return ResponseEntity.status(HttpStatus.CREATED).body(device)
    }

    @GetMapping
    fun getDevices(
        @RequestParam(required = false) homeId: Long?,
        @RequestParam(required = false) roomId: Long?,
        @RequestParam(required = false) type: DeviceType?,
    ): List<DeviceResponse> {
        return deviceService.getAllDevices(homeId, roomId, type)
    }

    @GetMapping("/{deviceId}")
    fun getDevice(@PathVariable deviceId: String): ResponseEntity<DeviceResponse> {
        val device = deviceService.getDevice(deviceId)
        return if (device != null) {
            ResponseEntity.ok(device)
        } else {
            ResponseEntity.notFound().build()
        }
    }

    @PatchMapping("/{deviceId}")
    fun updateDevice(
        @PathVariable deviceId: String,
        @Valid @RequestBody request: UpdateDeviceRequest
    ): ResponseEntity<DeviceResponse> {
        val device = deviceService.updateDevice(deviceId, request)
        return if (device != null) {
            ResponseEntity.ok(device)
        } else {
            ResponseEntity.notFound().build()
        }
    }

    @DeleteMapping("/{deviceId}")
    fun deleteDevice(@PathVariable deviceId: String): ResponseEntity<Void> {
        val deleted = deviceService.deleteDevice(deviceId)
        return if (deleted) {
            ResponseEntity.noContent().build()
        } else {
            ResponseEntity.notFound().build()
        }
    }
}