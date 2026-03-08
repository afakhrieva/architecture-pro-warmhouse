FROM golang:1.22-alpine AS builder

WORKDIR /app

# Копируем файлы с исходным кодом
COPY go.mod ./
COPY *.go ./

# Собираем приложение
RUN go build -o api-gateway

# Финальный образ
FROM alpine:latest

WORKDIR /app

# Копируем скомпилированное приложение из builder
COPY --from=builder /app/api-gateway .

# Порт приложения
EXPOSE 8080

# Запуск
CMD ["./api-gateway"]