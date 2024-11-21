from pydantic import BaseModel, ConfigDict


class DrugGroupSchema(BaseModel):
    id: int
    displayName: str
    description: str


class DrugFieldsSchema(BaseModel):
    displayName: str
    medicine_prescriptions: list[DrugGroupSchema]


class DrugGroupFieldsResponse(DrugFieldsSchema):
    pass
    # medicine_prescriptions: list[DrugFieldsSchema]
