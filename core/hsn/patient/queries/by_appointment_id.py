from pydantic import ValidationError
from sqlalchemy import select, exc
from sqlalchemy.orm import selectinload

from api.decorators import HandleExceptions
from api.exceptions import (
    NotFoundException,
    InternalServerException,
    ValidationException,
)
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.purpose.commands.create import check_appointment_exists
from core.hsn.patient.commands.create import convert_to_patient_response
from core.hsn.patient.schemas import PatientResponse, PatientResponseWithoutFullName
from shared.db.db_session import session
from shared.db.models.patient import PatientDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel


async def hsn_get_patient_by_appointment_id(appointment_id: int):
    await check_appointment_exists(appointment_id)
    query = (
        select(AppointmentDBModel)
        .options(
            selectinload(AppointmentDBModel.patient),
            selectinload(AppointmentDBModel.patient).selectinload(
                PatientDBModel.contragent
            ),
        )
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await session.execute(query)
    appointment = cursor.scalars().first()
    patient_response = await convert_to_patient_response(
        appointment.patient, type="without"
    )

    return PatientResponseWithoutFullName.model_validate(patient_response)
