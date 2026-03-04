# Dockerfile
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только зависимости сначала (для кэширования)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Создаём непривилегированного пользователя
RUN addgroup --system --gid 1001 app && \
    adduser --system --uid 1001 --gid 1001 app

# Копируем всё приложение
COPY --chown=app:app ./app ./app
COPY --chown=app:app run.py .

# Переключаемся на непривилегированного пользователя
USER app

# Порт приложения
EXPOSE 8001

# Запуск
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]