from fastapi import Request, HTTPException
from functools import wraps
from loguru import logger


def admin_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = None

        request = kwargs.get('request')

        if not request:
            raise HTTPException(status_code=400, detail="Request Object not found")

        user_role = request.user.role
        if user_role != "admin":
            raise HTTPException(status_code=403, detail="Доступ запрещен!")

        return await func(*args, **kwargs)

    return wrapper
