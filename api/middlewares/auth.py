from starlette.requests import HTTPConnection

from domains.core.user import hsn_user_get_me
from domains.core.user.model import User
from infra import config
import jwt
from typing import Optional, Tuple
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> Tuple[bool, Optional[User]]:
        curr_user = None
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, curr_user

        try:
            scheme, creds = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, curr_user
        except ValueError:
            return False, curr_user

        if not creds:
            return False, curr_user

        try:
            payload = jwt.decode(
                creds,
                config.JWT_SECRET,
                algorithms=[config.JWT_ALGORITHM],
            )
            user_id = payload.get("user_id")
        except jwt.exceptions.PyJWTError:
            return False, curr_user

        curr_user = await hsn_user_get_me(user_id)
        return True, curr_user


class AuthMiddleware(BaseAuthenticationMiddleware):
    pass
