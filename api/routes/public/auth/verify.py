from .router import auth_router
from pydantic import BaseModel, Field
from fastapi import Response
from utils import jwt_decode


class AuthVerifyTokenRequest(BaseModel):
    token: str = Field(..., description="token")


@auth_router.post(
    '/verify',
)
async def verify_user(body: AuthVerifyTokenRequest):
    jwt_decode(body.token)
    return Response(status_code=200)
