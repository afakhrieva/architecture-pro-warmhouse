from fastapi import Header, HTTPException
from uuid import UUID
from typing import Optional

async def get_current_user_id(
    x_user_id: Optional[str] = Header(None, description="User ID from API Gateway")
) -> UUID:
    """Получает ID пользователя из заголовка (добавлен API Gateway)"""
    if not x_user_id:
        raise HTTPException(
            status_code=401,
            detail="X-User-ID header is required"
        )

    try:
        return UUID(x_user_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid X-User-ID format (must be UUID)"
        )

def get_db():
    from app.db.memory_db import db
    return db