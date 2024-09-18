from loguru import logger
from sqlalchemy import select, exc
from sqlalchemy.orm import selectinload

from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat
from core.hsn.appointment.blocks.purpose.commands.create import check_appointment_exists
from core.hsn.appointment.blocks.purpose.model import AppointmentPurposeResponseFlat, MedicineGroupData
from shared.db.models import MedicinesPrescriptionDBModel, DrugDBModel
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from shared.db.db_session import db_session, SessionContext


@SessionContext()
async def hsn_query_purposes_by_appointment_id(appointment_id: int):
    results_dict = dict()
    await check_appointment_exists(appointment_id)
    query = (
        select(AppointmentPurposeDBModel)
        .options(selectinload(AppointmentPurposeDBModel.medicine_prescriptions).selectinload(
            MedicinesPrescriptionDBModel.drug).selectinload(DrugDBModel.drug_group))
        .where(AppointmentPurposeDBModel.appointment_id == appointment_id)
        .where(AppointmentPurposeDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    purposes = cursor.scalars().all()
    if len(purposes) == 0:
        raise NotFoundException(message="У приема нет блока назначений лекарственных препаратов")

    for purpose in purposes:
        for med_prescription in purpose.medicine_prescriptions:
            if med_prescription.drug.drug_group:
                drug_group_name = med_prescription.drug.drug_group.name
                results_dict[drug_group_name] = {
                    "id": med_prescription.drug.id,
                    "dosa": med_prescription.dosa,
                    "note": med_prescription.note or "",
                    "name": med_prescription.drug.name
                }

    return results_dict
