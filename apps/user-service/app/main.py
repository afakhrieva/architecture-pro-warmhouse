# app/main.py
from fastapi import FastAPI
from app.api import users, homes, locations

app = FastAPI(
    title="User Service",
    version="1.0.0",
    description="Управление пользователями, домами и комнатами"
)

# Подключаем все роутеры
app.include_router(users.router)
app.include_router(homes.router)
app.include_router(locations.router)

@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {
        "status": "ok",
        "service": "user-service"
    }

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "User Service API",
        "docs": "/docs"
    }