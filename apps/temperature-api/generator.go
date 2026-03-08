package main

import (
	"math/rand"
	"time"
)

type TemperatureGenerator struct {
	min                  float64
	max                  float64
	sensorInfo           map[string]SensorInfo
	sensorInfoBySensorId map[string]SensorInfo
}

func NewTemperatureGenerator() *TemperatureGenerator {
	rand.New(rand.NewSource(time.Now().UnixNano()))

	// Словарь с информацией о датчиках по локациям
	sensorInfo := map[string]SensorInfo{
		"living_room": {
			SensorType:  "temperature",
			SensorID:    "1",
			Description: "Датчик температуры в гостиной",
			Location:    "Living Room",
		},
		"bedroom": {
			SensorType:  "temperature",
			SensorID:    "2",
			Description: "Датчик температуры в спальне",
			Location:    "Bedroom",
		},
		"kitchen": {
			SensorType:  "temperature",
			SensorID:    "3",
			Description: "Датчик температуры на кухне",
			Location:    "Kitchen",
		},
		"unknown": {
			SensorType:  "unknown",
			SensorID:    "0",
			Description: "Неизвестный тип датчика",
			Location:    "Unknown",
		},
	}

	locationBySensorId := make(map[string]SensorInfo)
	for _, value := range sensorInfo {
		locationBySensorId[value.SensorID] = value
	}

	return &TemperatureGenerator{
		min:                  -10.0,
		max:                  35.0,
		sensorInfo:           sensorInfo,
		sensorInfoBySensorId: locationBySensorId,
	}
}

func (g *TemperatureGenerator) Generate() float64 {
	temp := g.min + rand.Float64()*(g.max-g.min)
	// Округляем до 1 знака после запятой
	return float64(int(temp*10)) / 10
}

func (g *TemperatureGenerator) GetSensorInfoByLocation(location string) (
	sensorId string,
	sensorType string,
	description string,
) {
	info, exists := g.sensorInfo[location]
	if !exists {
		info = g.sensorInfo["unknown"]
	}
	return info.SensorID, info.SensorType, info.Description
}

func (g *TemperatureGenerator) GetSensorInfoBySensorId(sensorId string) (
	location string,
	sensorType string,
	description string,
) {
	info, exists := g.sensorInfoBySensorId[sensorId]
	if !exists {
		info = g.sensorInfoBySensorId["0"]
	}
	return info.Location, info.SensorType, info.Description
}
