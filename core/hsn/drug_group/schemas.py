from pydantic import BaseModel, ConfigDict


class DrugGroupSchema(BaseModel):
    id: int
    displayName: str
    description: str


class DrugGroupFieldsResponse(BaseModel):
    displayName: str
    drugs: list[DrugGroupSchema]
