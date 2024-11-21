from api.exceptions.base import UnprocessableEntityException, ForbiddenException
from shared.db.db_session import db_session, SessionContext
from shared.db.models import CabinetDBModel, DoctorDBModel, lgotadrugs
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.patient import PatientDBModel
from pydantic import BaseModel, ValidationError
from core.hsn.patient.model import (
    Patient,
    PatientResponse,
    PatientAppointmentHistoryDto,
    PatientWithAppointmentHistoryResponse,
)
from sqlalchemy import select, exc, desc, Result
from sqlalchemy.orm import joinedload, selectinload
from api.exceptions import (
    NotFoundException,
    ValidationException,
    InternalServerException,
)
from loguru import logger
from sqlalchemy import text

from shared.db.queries import db_query_entity_by_id
from ..commands.create import convert_to_patient_response
from ..model import Contragent, PatientWithoutFullNameResponse
from utils import contragent_hasher
from shared.db.models.contragent import ContragentDBModel


async def get_patient_appointment_history(doctor_id: int, patient_id: int):
    patient_model: PatientDBModel = await db_query_entity_by_id(
        PatientDBModel, patient_id
    )
    doctor_model: DoctorDBModel = await db_query_entity_by_id(DoctorDBModel, doctor_id)

    if patient_model.cabinet_id != doctor_model.cabinet_id:
        raise ForbiddenException(
            "У вас нет прав для доступа к пациенту с id:{}".format(patient_model.id)
        )

    query = (
        select(AppointmentDBModel.id.label("id"), AppointmentDBModel.date.label("date"))
        .where(
            AppointmentDBModel.patient_id == patient_model.id,
            AppointmentDBModel.doctor_id == doctor_model.id,
            AppointmentDBModel.is_deleted.is_(False),
        )
        .order_by(desc(AppointmentDBModel.created_at))
    )
    cursor: Result = await db_session.execute(query)
    appointments = cursor.all()
    if not appointments:
        return []
    result = [
        PatientAppointmentHistoryDto(id=appointment[0], date=appointment[1])
        for appointment in appointments
    ]
    return result


@SessionContext()
async def hsn_query_patient_by_id(
    doctor_id: int, patient_id: int
) -> PatientWithoutFullNameResponse:
    query = (
        select(PatientDBModel)
        .options(
            selectinload(PatientDBModel.cabinet).selectinload(CabinetDBModel.doctors)
        )
        .options(selectinload(PatientDBModel.contragent))
        .where(DoctorDBModel.id == doctor_id)
        .where(PatientDBModel.id == patient_id)
        .where(PatientDBModel.is_deleted.is_(False))
    )

    cursor = await db_session.execute(query)
    patient = cursor.scalars().first()

    appointment_histories = await get_patient_appointment_history(doctor_id, patient_id)
    converted_patient = await convert_to_patient_response(patient, type="without")

    result = PatientWithAppointmentHistoryResponse(
        appointment_histories=appointment_histories,
        id=converted_patient.id,
        name=converted_patient.name,
        last_name=converted_patient.last_name,
        patronymic=converted_patient.patronymic,
        gender=converted_patient.gender,
        age=converted_patient.age,
        birth_date=converted_patient.birth_date,
        dod=converted_patient.dod,
        location=converted_patient.location,
        district=converted_patient.district,
        address=converted_patient.address,
        phone=converted_patient.phone,
        clinic=converted_patient.clinic,
        referring_doctor=converted_patient.referring_doctor,
        referring_clinic_organization=converted_patient.referring_clinic_organization,
        disability=converted_patient.disability,
        lgota_drugs=converted_patient.lgota_drugs,
        has_hospitalization=converted_patient.has_hospitalization,
        count_hospitalization=converted_patient.count_hospitalization,
        last_hospitalization_date=converted_patient.last_hospitalization_date,
        patient_note=converted_patient.patient_note,
    )

    return PatientWithAppointmentHistoryResponse.model_validate(result)
