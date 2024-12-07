from typing import Type, TypeVar
from .db_model import BaseDBModel
from pydantic import BaseModel

DBModelType = TypeVar("DBModelType", bound=BaseDBModel)
ModelType = TypeVar("ModelType", bound=BaseModel)
