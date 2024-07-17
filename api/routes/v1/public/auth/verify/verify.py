from .router import auth_verify_router
from pydantic import BaseModel, Field
from fastapi import Response
from utils import JWTHelper


class AuthVerifyTokenRequest(BaseModel):
    token: str = Field(..., description="token")


@auth_verify_router.post(
    '',
    summary="Верификация пользователя"
)
async def verify_user(body: AuthVerifyTokenRequest):
    JWTHelper.jwt_decode(body.token)
    return Response(status_code=200)
