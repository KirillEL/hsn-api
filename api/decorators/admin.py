from fastapi import Request, HTTPException
from functools import wraps
from loguru import logger


def admin_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = None

        request = kwargs.get("request")

        if not request:
            raise HTTPException(status_code=400, detail="Request Object not found")

        user_roles = request.user.roles
        is_admin = False
        for role in user_roles:
            if role.name == "admin":
                is_admin = True
                break

        if not is_admin:
            raise HTTPException(status_code=403, detail="Вы не администратор")

        return await func(*args, **kwargs)

    return wrapper
