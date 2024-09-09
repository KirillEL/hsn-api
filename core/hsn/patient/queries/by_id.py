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
async def hsn_get_patient_by_id(doctor_id: int, patient_id: int):
    query = (
        select(PatientDBModel)
        .options(joinedload(PatientDBModel.cabinet)
                 .joinedload(CabinetDBModel.doctors)
                 , joinedload(PatientDBModel.contragent))
        .where(DoctorDBModel.id == doctor_id)
        .where(PatientDBModel.id == patient_id)
    )

    try:
        cursor = await db_session.execute(query)
        patient = cursor.scalars().first()
    except exc.NoResultFound as nrf:
        logger.error(f"No patient was found: {nrf}")
        raise NotFoundException(
            message=f"Пациент с id: {patient_id} не найден"
        )
    except exc.SQLAlchemyError as sqle:
        logger.error(f"Failed to get patient: {sqle}")
        raise InternalServerException(
            message="Ошибка сервера: не удалось выполнить запрос для получения пациента"
        )

    converted_patient = await convert_to_patient_response(patient, type="without")
    return PatientResponseWithoutFullName.model_validate(converted_patient)
