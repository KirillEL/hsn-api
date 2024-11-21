from sqlalchemy import select, exc
from sqlalchemy.orm import selectinload

from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import ForbiddenException
from shared.db.models import MedicinesPrescriptionDBModel, DrugDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from shared.db.db_session import db_session, SessionContext
from shared.db.queries import db_query_entity_by_id


@SessionContext()
async def hsn_query_purposes_by_appointment_id(doctor_id: int, appointment_id: int):
    results_dict = {}
    appointment = await db_query_entity_by_id(AppointmentDBModel, appointment_id)
    if not appointment:
        raise NotFoundException(
            message="Прием c id: {} не найден".format(appointment_id)
        )

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException(
            "У вас нет прав для доступа к приему с id:{}".format(appointment_id)
        )

    query = (
        select(AppointmentPurposeDBModel)
        .options(
            selectinload(AppointmentPurposeDBModel.medicine_prescriptions)
            .selectinload(MedicinesPrescriptionDBModel.drug)
            .selectinload(DrugDBModel.drug_group)
        )
        .where(AppointmentPurposeDBModel.appointment_id == appointment_id)
        .where(AppointmentPurposeDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    purposes = cursor.scalars().all()
    if len(purposes) == 0:
        return None

    for purpose in purposes:
        for med_prescription in purpose.medicine_prescriptions:
            if med_prescription.drug.drug_group:
                drug_group_name = med_prescription.drug.drug_group.name
                results_dict[drug_group_name] = {
                    "id": med_prescription.drug.id,
                    "dosa": med_prescription.dosa,
                    "note": med_prescription.note or "",
                    "name": med_prescription.drug.name,
                }

    return results_dict
