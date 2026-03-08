package ru.yandex.practicum.arch.smarthome.deviceservice.service

import java.time.ZoneId
import java.time.format.DateTimeFormatter

val DATE_FORMATTER: DateTimeFormatter = DateTimeFormatter.ISO_DATE_TIME.withZone(ZoneId.systemDefault())