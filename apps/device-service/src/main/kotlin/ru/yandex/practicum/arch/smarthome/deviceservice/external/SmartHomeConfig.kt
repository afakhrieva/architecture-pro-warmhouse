package ru.yandex.practicum.arch.smarthome.deviceservice.external

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.http.client.SimpleClientHttpRequestFactory
import org.springframework.web.client.RestTemplate
import java.time.Duration

@Configuration
class SmartHomeConfig {

    @Bean
    fun smartHomeRestTemplate(): RestTemplate {
        val factory = SimpleClientHttpRequestFactory().apply {
            setConnectTimeout(Duration.ofSeconds(5))
            setReadTimeout(Duration.ofSeconds(5))
        }

        val restTemplate = RestTemplate(factory)

        restTemplate.interceptors.add { request, body, execution ->
            request.headers.set("User-Agent", "Device-Service/1.0")
            execution.execute(request, body)
        }

        return restTemplate
    }
}