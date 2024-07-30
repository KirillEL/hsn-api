from sqlalchemy import select, not_

from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.purpose.commands.create import check_appointment_exists
from core.hsn.appointment.blocks.purpose.model import (
    AppointmentPurposeResponseFlat,
    MedicineGroupData,
)
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from shared.db.db_session import session


async def hsn_get_purposes_by_appointment_id(appointment_id: int):
    results_dict = dict()
    await check_appointment_exists(appointment_id)
    query = (
        select(AppointmentPurposeDBModel)
        .where(AppointmentPurposeDBModel.appointment_id == appointment_id)
        .where(not_(AppointmentPurposeDBModel.is_deleted))
    )
    cursor = await session.execute(query)
    purposes = cursor.scalars().all()
    if len(purposes) == 0:
        raise NotFoundException(
            message="У приема нет блока назначений лекарственных препаратов"
        )

    results: list[AppointmentPurposeResponseFlat] = []
    for purpose in purposes:
        final_result = AppointmentPurposeResponseFlat(
            medicine_group=purpose.medicine_prescription.medicine_group.name,
            medicine_group_data=MedicineGroupData(
                id=purpose.medicine_prescription.id,
                name=purpose.medicine_prescription.name,
                dosa=purpose.dosa,
                note=purpose.note,
            ),
        )
        results.append(final_result)
        for r in results:
            results_dict[r.medicine_group] = r.medicine_group_data
    return results_dict
