package ru.yandex.practicum.arch.smarthome.deviceservice.external

import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.core.ParameterizedTypeReference
import org.springframework.http.HttpMethod
import org.springframework.http.ResponseEntity
import org.springframework.stereotype.Service
import org.springframework.web.client.RestTemplate
import org.springframework.web.client.getForObject
import org.springframework.web.client.patchForObject
import org.springframework.web.client.postForObject

@Service
class SmartHomeClient (
    @Value("\${smart-home.base-url:http://smart-home:8080}")
    private val baseUrl: String,
    private val smartHomeRestTemplate: RestTemplate
) {

    private val logger = LoggerFactory.getLogger(javaClass)

    /**
     * GET /api/v1/sensors - получить все датчики
     */
    fun getAllSensors(): List<SmartHomeSensor> {
        return try {
           val url = "$baseUrl/api/v1/sensors"
            logger.debug("GET $url")

            val responseType = object : ParameterizedTypeReference<List<SmartHomeSensor>>() {}
            val response: ResponseEntity<List<SmartHomeSensor>> = smartHomeRestTemplate.exchange(
                url,
                HttpMethod.GET,
                null,
                responseType
            )

            response.body ?: emptyList()

        } catch (e: Exception) {
            logger.error("Ошибка при получении датчиков из монолита: ${e.message}")
            emptyList()  // Возвращаем пустой список, чтобы не ломать основной поток
        }
    }

    /**
     * GET /api/v1/sensors/{id} - получить конкретный датчик
     */
    fun getSensor(id: String): SmartHomeSensor? {
        return try {
            val url = "$baseUrl/api/v1/sensors/$id"
            logger.debug("GET $url")

            smartHomeRestTemplate.getForObject<SmartHomeSensor>(url)

        } catch (e: Exception) {
            logger.error("Ошибка при получении датчика $id из монолита: ${e.message}")
            null
        }
    }

    /**
     * POST /api/v1/sensors - создать новый датчик
     */
    fun createSensor(request: CreateSensorRequest): SmartHomeSensor? {
        return try {
            val url = "$baseUrl/api/v1/sensors"
            logger.info("POST $url - создание нового датчика: ${request.name}")

            smartHomeRestTemplate.postForObject<SmartHomeSensor>(url, request)

        } catch (e: Exception) {
            logger.error("Ошибка при создании датчика в монолите: ${e.message}")
            null
        }
    }

    /**
     * PATCH /api/v1/sensors/{id}/value - обновить значение датчика
     */
    fun updateSensorValue(id: String, value: Double): Boolean {
        return try {
            val url = "$baseUrl/api/v1/sensors/$id/value"
            val request = mapOf("value" to value)

            logger.debug("PATCH $url - новое значение: $value")

            smartHomeRestTemplate.patchForObject<String>(url, request)
            true

        } catch (e: Exception) {
            logger.error("Ошибка при обновлении значения датчика $id: ${e.message}")
            false
        }
    }

    /**
     * DELETE /api/v1/sensors/{id} - удалить датчик
     */
    fun deleteSensor(id: String): Boolean {
        return try {
            val url = "$baseUrl/api/v1/sensors/$id"
            logger.info("DELETE $url")

            smartHomeRestTemplate.delete(url)
            true

        } catch (e: Exception) {
            logger.error("Ошибка при удалении датчика $id: ${e.message}")
            false
        }
    }

    fun isSmartHomeAppAvailable(): Boolean {
        return try {
            val url = "$baseUrl/api/v1/health"
            smartHomeRestTemplate.getForObject<String>(url)
            true
        } catch (e: Exception) {
            false
        }
    }
}