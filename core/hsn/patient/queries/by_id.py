from api.decorators import HandleExceptions
from api.exceptions.base import UnprocessableEntityException
from shared.db.db_session import db_session, SessionContext
from shared.db.models import CabinetDBModel, DoctorDBModel
from shared.db.models.patient import PatientDBModel
from pydantic import BaseModel, ValidationError
from core.hsn.patient.model import Patient, PatientResponse
from sqlalchemy import select, exc
from sqlalchemy.orm import joinedload
from api.exceptions import NotFoundException, ValidationException, InternalServerException
from loguru import logger

from ..commands.create import convert_to_patient_response
from ..model import Contragent, PatientResponseWithoutFullName
from utils import contragent_hasher
from shared.db.models.contragent import ContragentDBModel


@SessionContext()
@HandleExceptions()
async def hsn_get_patient_by_id(current_user_id: int, patient_id: int):
    query = (
        select(PatientDBModel, PatientDBModel.author_id)
        .options(joinedload(PatientDBModel.cabinet)
                 .joinedload(CabinetDBModel.doctors)
                 , joinedload(PatientDBModel.contragent))
        .where(DoctorDBModel.user_id == current_user_id)
        .where(PatientDBModel.id == patient_id)
    )
    cursor = await db_session.execute(query)
    patient, author_id = cursor.first()

    if author_id != current_user_id:
        raise NotFoundException

    if not patient:
        raise NotFoundException(message="Пациент с таким id не найден!")

    converted_patient = await convert_to_patient_response(patient, type="without")
    return PatientResponseWithoutFullName.model_validate(converted_patient)
