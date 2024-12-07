from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.exceptions import (
    NotFoundException,
)
from api.exceptions.base import ForbiddenException
from domains.core.hsn.patient.commands.create import convert_to_patient_response
from domains.core.hsn.patient.model import PatientWithoutFullNameResponse
from domains.shared.db.db_session import db_session, SessionContext
from domains.shared.db.models.patient import PatientDBModel
from domains.shared.db.models.appointment.appointment import AppointmentDBModel
from domains.shared.db.queries import db_query_entity_by_id


@SessionContext()
async def hsn_query_patient_by_appointment_id(
    appointment_id: int, doctor_id: int = None
) -> PatientWithoutFullNameResponse:
    appointment = await db_query_entity_by_id(AppointmentDBModel, appointment_id)
    if not appointment:
        raise NotFoundException(message="Прием не найден")

    if appointment.author_id != doctor_id:
        raise ForbiddenException(
            message=f"У вас нет прав к получению приема с id: {appointment_id}"
        )

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

    cursor = await db_session.execute(query)
    appointment = cursor.scalars().first()

    patient_response = await convert_to_patient_response(
        appointment.patient, type="without"
    )

    return PatientWithoutFullNameResponse.model_validate(patient_response)
