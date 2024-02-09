from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    login: str = None
    password: str
    role: str
    is_deleted: bool


class UserFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    login: str
    role: str
    is_deleted: bool


class UserAuthor(UserFlat):
    pass

