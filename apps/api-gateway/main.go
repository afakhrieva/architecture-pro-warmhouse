package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"
)

var services = map[string]string{
	"/users":          "http://user-service:8001",
	"/devices":        "http://device-service:8002",
	"/telemetry":      "http://telemetry-service:8003",
	"/api/v1/sensors": "http://smart-home:8003", // запросы в монолит
	"/temperature":    "http://smart-home:8003", // запросы в монолит
}

func main() {
	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/", proxyHandler)

	fmt.Println("API Gateway запущен на порту 8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, `{"status":"ok","service":"api-gateway"}`)
}

func proxyHandler(w http.ResponseWriter, r *http.Request) {
	// Пропускаем health check
	if r.URL.Path == "/health" {
		return
	}

	// Ищем сервис
	for prefix, target := range services {
		if strings.HasPrefix(r.URL.Path, prefix) {
			proxyRequest(w, r, target)
			return
		}
	}

	http.Error(w, "Service not found", http.StatusNotFound)
}

func proxyRequest(w http.ResponseWriter, r *http.Request, target string) {
	// Создаем URL
	url := target + r.URL.Path
	if r.URL.RawQuery != "" {
		url += "?" + r.URL.RawQuery
	}

	// Создаем запрос
	proxyReq, _ := http.NewRequest(r.Method, url, r.Body)
	proxyReq.Header = r.Header.Clone()

	log.Printf(url)

	// Отправляем
	client := &http.Client{}
	resp, err := client.Do(proxyReq)
	if err != nil {
		http.Error(w, "Service unavailable", http.StatusServiceUnavailable)
		return
	}
	defer resp.Body.Close()

	// Копируем ответ
	for k, v := range resp.Header {
		w.Header()[k] = v
	}
	w.WriteHeader(resp.StatusCode)
	io.Copy(w, resp.Body)

	log.Printf("%s %s -> %s %d", r.Method, r.URL.Path, target, resp.StatusCode)
}
