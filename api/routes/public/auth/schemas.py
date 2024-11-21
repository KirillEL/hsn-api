from pydantic import BaseModel, Field


class AuthLoginResponse(BaseModel):
    token: str = Field(..., description="token")
