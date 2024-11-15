from typing import List

from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from core.hsn.appointment import HsnAppointmentListContext
from core.hsn.appointment.model import PatientAppointmentFlat, PatientFlatForAppointmentList
from shared.db.db_session import SessionContext, db_session
from shared.db.models import PatientDBModel, MedicinesPrescriptionDBModel, DrugDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from utils import contragent_hasher


@SessionContext()
async def hsn_query_appointment_with_blocks_list(
        context: HsnAppointmentListContext
):
    query = (
        select(AppointmentDBModel)
        .where(AppointmentDBModel.doctor_id == context.doctor_id)
        .options(
            selectinload(AppointmentDBModel.patient)
            .selectinload(PatientDBModel.contragent)
        )
        .options(
            selectinload(AppointmentDBModel.block_complaint),
            selectinload(AppointmentDBModel.block_ekg),
            selectinload(AppointmentDBModel.block_diagnose),
            selectinload(AppointmentDBModel.block_laboratory_test),
            selectinload(AppointmentDBModel.block_clinical_condition)
        )
        .options(
            selectinload(AppointmentDBModel.purposes)
            .selectinload(AppointmentPurposeDBModel.medicine_prescriptions)
            .selectinload(MedicinesPrescriptionDBModel.drug)
            .selectinload(DrugDBModel.drug_group)
        )
    )

    query = query.order_by(desc(AppointmentDBModel.created_at))

    cursor = await db_session.execute(query)
    patient_appointments = cursor.scalars().all()

    results: List[PatientAppointmentFlat] = []
    for appointment in patient_appointments:
        patient_info = PatientFlatForAppointmentList(
            name=contragent_hasher.decrypt(appointment.patient.contragent.name),
            last_name=contragent_hasher.decrypt(appointment.patient.contragent.last_name),
            patronymic=contragent_hasher.decrypt(
                appointment.patient.contragent.patronymic) if appointment.patient.contragent.patronymic else ""
        )

        appointment_flat = PatientAppointmentFlat(
            id=appointment.id,
            full_name=f'{patient_info.name} {patient_info.last_name} {patient_info.patronymic or ""}'.rstrip(),
            doctor_id=appointment.doctor_id,
            date=appointment.date,
            date_next=str(appointment.date_next) if appointment.date_next else None,
            block_laboratory_test=appointment.block_laboratory_test,
            block_diagnose=appointment.block_diagnose,
            block_ekg=appointment.block_ekg,
            block_complaint=appointment.block_complaint,
            block_clinical_condition=appointment.block_clinical_condition,
            purposes=appointment.purposes,
            status=appointment.status
        )
        results.append(appointment_flat)

    return results

