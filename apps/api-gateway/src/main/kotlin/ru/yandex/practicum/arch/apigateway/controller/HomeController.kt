package ru.yandex.practicum.arch.apigateway.controller

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@RestController
class HomeController {
    @GetMapping("/")
    fun home(): Map<String, Any> = mapOf(
        "service" to "API Gateway",
        "version" to "1.0.0",
        "routes" to listOf(
            "/api/users/** → user-service:8001",
            "/api/devices/** → device-service:8002",
            "/api/telemetry/** → telemetry-service:8003",
            "/api/v1/sensors/** → smart-home:8080 (legacy)",
            "/health → health check"
        )
    )
}