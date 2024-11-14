from api.exceptions.base import UnprocessableEntityException
from shared.db.db_session import db_session, SessionContext
from shared.db.models import CabinetDBModel, DoctorDBModel
from shared.db.models.patient import PatientDBModel
from pydantic import BaseModel, ValidationError
from core.hsn.patient.model import Patient, PatientResponse
from sqlalchemy import select, exc
from sqlalchemy.orm import joinedload, selectinload
from api.exceptions import NotFoundException, ValidationException, InternalServerException
from loguru import logger
from sqlalchemy import text
from ..commands.create import convert_to_patient_response
from ..model import Contragent, PatientWithoutFullNameResponse
from utils import contragent_hasher
from shared.db.models.contragent import ContragentDBModel


@SessionContext()
async def hsn_query_patient_by_id(doctor_id: int, patient_id: int) -> PatientWithoutFullNameResponse:
    query = (
        select(PatientDBModel)
        .options(
            selectinload(PatientDBModel.cabinet)
            .selectinload(CabinetDBModel.doctors)
        )
        .options(
            selectinload(PatientDBModel.contragent)
        )
        .where(DoctorDBModel.id == doctor_id)
        .where(PatientDBModel.id == patient_id)
        .where(PatientDBModel.is_deleted.is_(False))
    )

    cursor = await db_session.execute(query)
    patient = cursor.scalars().first()

    converted_patient = await convert_to_patient_response(patient, type="without")
    return PatientWithoutFullNameResponse.model_validate(converted_patient)
