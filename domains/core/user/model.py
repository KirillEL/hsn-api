from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    login: str = None
    password: str
    is_deleted: bool


class Role(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class UserFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    login: str
    roles: list[Role]
    is_deleted: bool


class UserWithPasswordFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    login: str
    password: str
    roles: list[Role]


class UserAuthor(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    login: str
    is_deleted: bool
