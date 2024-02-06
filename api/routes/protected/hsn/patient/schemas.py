from pydantic import BaseModel, Field
from typing import Optional

from sqlalchemy import Date


class PatientResponse(BaseModel):
    id: int
    name: str
    last_name: str
    patronymic: Optional[str] = None

    birth_date: str
    age: int
    gender: str

    # Дописать надо будет