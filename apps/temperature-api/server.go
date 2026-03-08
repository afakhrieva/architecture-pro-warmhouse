package main

import (
	"log"
	"net/http"
)

type Server struct {
	handler *TemperatureHandler
}

func NewServer() *Server {
	return &Server{
		handler: NewTemperatureHandler(),
	}
}

func (s *Server) Start(addr string) {
	http.HandleFunc("/temperature", s.handler.HandleByLocation)  // GET /temperature?location=...
	http.HandleFunc("/temperature/", s.handler.HandleBySensorID) // GET /temperature/{sensorId}

	log.Printf("Server starting on %s", addr)
	log.Fatal(http.ListenAndServe(addr, nil))
}
