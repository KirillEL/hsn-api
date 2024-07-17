from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User(Base):
    id: int
    is_active: bool
    login: str
    password: str
    is_deleted: bool


class Role(Base):
    id: int
    name: str


class UserFlat(Base):
    id: int
    login: str
    roles: list[Role]
    is_deleted: bool


class UserWithPasswordFlat(Base):
    id: int
    login: str
    password: str
    roles: list[Role]


class UserAuthor(Base):
    id: int
    login: str
    is_deleted: bool
