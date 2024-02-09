from .router import auth_router
from .schemas import AuthLoginResponse
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field
from core.user.queries import user_query_login
from utils import jwt_encode
from api.exceptions import UserNotFoundException
from fastapi import Response


class AuthRequest(BaseModel):
    login: str = Field(..., description="login")
    password: str = Field(..., description="password")



@auth_router.post(
    "/login",
    response_model=AuthLoginResponse,
    responses={"404": {"model": ExceptionResponseSchema}}
)
async def login_user(req: AuthRequest):
    user = await user_query_login(req.login, req.password)
    if user is None:
        raise UserNotFoundException
    
    token = AuthLoginResponse(
        token=jwt_encode(payload={"user_id": user.id}),
    )
    return {"token": token.token}
