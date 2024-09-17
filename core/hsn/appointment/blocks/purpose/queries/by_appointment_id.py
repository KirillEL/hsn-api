from loguru import logger
from sqlalchemy import select, exc
from sqlalchemy.orm import selectinload

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat
from core.hsn.appointment.blocks.purpose.commands.create import check_appointment_exists
from core.hsn.appointment.blocks.purpose.model import AppointmentPurposeResponseFlat, MedicineGroupData
from shared.db.models import MedicinesPrescriptionDBModel
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from shared.db.db_session import db_session, SessionContext


@SessionContext()
@HandleExceptions()
async def hsn_get_purposes_by_appointment_id(appointment_id: int):
    results_dict = dict()
    await check_appointment_exists(appointment_id)
    query = (
        select(AppointmentPurposeDBModel)
        .options(selectinload(AppointmentPurposeDBModel.medicine_prescriptions).selectinload(
            MedicinesPrescriptionDBModel.medicine_group))
        .where(AppointmentPurposeDBModel.appointment_id == appointment_id)
        .where(AppointmentPurposeDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    purposes = cursor.scalars().all()
    if len(purposes) == 0:
        raise NotFoundException(message="У приема нет блока назначений лекарственных препаратов")

    results = []
    for purpose in purposes:
        logger.debug(f'purpose: {purpose.__dict__}')
        final_result = AppointmentPurposeResponseFlat(
            medicine_group=purpose.medicine_prescription.medicine_group.name,
            medicine_group_data=MedicineGroupData(
                id=purpose.medicine_prescription.id,
                name=purpose.medicine_prescription.name,
                dosa=purpose.dosa,
                note=purpose.note if purpose.note else ""
            )
        )
        results.append(final_result)
        for r in results:
            results_dict[r.medicine_group] = r.medicine_group_data
    return results_dict
