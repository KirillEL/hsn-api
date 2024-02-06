from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    login: str = None
    password: str


class UserFlat(BaseModel):
    id: int
    login: str

