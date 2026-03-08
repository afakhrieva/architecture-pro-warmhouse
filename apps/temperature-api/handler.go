package main

import (
	"encoding/json"
	"net/http"
	"strings"
	"time"
)

type TemperatureHandler struct {
	generator *TemperatureGenerator
}

func NewTemperatureHandler() *TemperatureHandler {
	return &TemperatureHandler{
		generator: NewTemperatureGenerator(),
	}
}

// Хендлер для GET /temperature?location=xxx
func (h *TemperatureHandler) HandleByLocation(w http.ResponseWriter, r *http.Request) {
	// Проверяем метод
	if r.Method != http.MethodGet {
		http.Error(w, "Only GET allowed", http.StatusMethodNotAllowed)
		return
	}

	// Получаем параметр location
	location := r.URL.Query().Get("location")
	if location == "" {
		http.Error(w, "location parameter is required", http.StatusBadRequest)
		return
	}

	sensorId, sensorType, description := h.generator.GetSensorInfoByLocation(location)

	// Формируем ответ
	response := TemperatureResponse{
		Value:       h.generator.Generate(),
		Unit:        "celsius",
		Timestamp:   time.Now(),
		Location:    location,
		Status:      "active",
		SensorID:    sensorId,
		SensorType:  sensorType,
		Description: description,
	}

	// Отправляем ответ
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// Хендлер для GET /temperature/{sensorId}
func (h *TemperatureHandler) HandleBySensorID(w http.ResponseWriter, r *http.Request) {
	// Проверяем метод
	if r.Method != http.MethodGet {
		http.Error(w, "Only GET allowed", http.StatusMethodNotAllowed)
		return
	}

	// Извлекаем sensorId из URL
	pathParts := strings.Split(r.URL.Path, "/")
	if len(pathParts) < 3 {
		http.Error(w, "sensorId is required", http.StatusBadRequest)
		return
	}

	sensorId := pathParts[2]
	if sensorId == "" {
		http.Error(w, "sensorId is required", http.StatusBadRequest)
		return
	}

	// Получаем данные по sensorId
	location, sensorType, description := h.generator.GetSensorInfoBySensorId(sensorId)

	// Формируем ответ
	response := TemperatureResponse{
		Value:       h.generator.Generate(),
		Unit:        "celsius",
		Timestamp:   time.Now(),
		Location:    location,
		Status:      "active",
		SensorID:    sensorId,
		SensorType:  sensorType,
		Description: description,
	}

	// Отправляем ответ
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}
