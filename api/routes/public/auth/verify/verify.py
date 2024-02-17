from .router import auth_verify_router
from pydantic import BaseModel, Field
from fastapi import Response
from utils import jwt_decode


class AuthVerifyTokenRequest(BaseModel):
    token: str = Field(..., description="token")


@auth_verify_router.post(
    '/',
)
async def verify_user(body: AuthVerifyTokenRequest):
    jwt_decode(body.token)
    return Response(status_code=200)
