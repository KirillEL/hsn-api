from pydantic import BaseModel, ConfigDict


class DrugGroupSchema(BaseModel):
    id: int
    displayName: str
    description: str


class DrugFieldsSchema(BaseModel):
    displayName: str
    drugs: list[DrugGroupSchema]


class DrugGroupFieldsResponse(BaseModel):
    medicine_prescriptions: list[DrugFieldsSchema]
