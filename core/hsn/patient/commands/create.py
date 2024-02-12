from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import insert
from shared.db.models.contragent import ContragentDBModel
from shared.db.models.patient import PatientDBModel
from core.hsn.patient import Patient


class HsnPatientCreateContext(BaseModel):
    user_id: int

    name: str
    last_name: str
    patronymic: Optional[str]
    age: int
    gender: str

    phone_number: int
    snils: str
    address: str


@SessionContext()
async def hsn_patient_create(context: HsnPatientCreateContext):
    # 1
    query_contragent = (
        insert(ContragentDBModel)
        .values(
            phone_number=context.phone_number,
            snils=context.snils,
            address=context.address
        )
        .returning(ContragentDBModel.id)
    )
    cursor = await db_session.execute(query_contragent)
    contragent_id = cursor.first()[0]

    # 2
    query_patient = (
        insert(PatientDBModel)
        .values(
            name=context.name,
            last_name=context.last_name,
            patronymic=context.patronymic,
            age=context.age,
            gender=context.gender,
            contragent_id=contragent_id
        )
        .returning(PatientDBModel)
    )
    cursor_2 = await db_session.execute(query_patient)
    new_patient = cursor_2.first()[0]
    return Patient.model_validate(new_patient)
