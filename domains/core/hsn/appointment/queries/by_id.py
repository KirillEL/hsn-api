from sqlalchemy import select, Select, Result
from sqlalchemy.orm import selectinload

from api.exceptions import (
    NotFoundException,
)
from api.exceptions.base import ForbiddenException
from domains.core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat
from domains.core.hsn.appointment.blocks.purpose.model import (
    MedicinePrescriptionFlat,
    MedicineGroupFlat,
)
from domains.core.hsn.appointment.model import (
    PatientFlatForAppointmentList,
    PatientAppointmentByIdDto,
    PatientInfoDto,
)
from domains.shared.db.db_session import db_session, SessionContext
from domains.shared.db.models import PatientDBModel, MedicinesPrescriptionDBModel, DrugDBModel
from domains.shared.db.models.appointment.appointment import AppointmentDBModel
from domains.shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from utils import contragent_hasher


async def build_patient_info(appointment: AppointmentDBModel):
    appointment.patient.contragent.name = contragent_hasher.decrypt(
        appointment.patient.contragent.name
    )
    appointment.patient.contragent.last_name = contragent_hasher.decrypt(
        appointment.patient.contragent.last_name
    )
    if appointment.patient.contragent.patronymic:
        appointment.patient.contragent.patronymic = contragent_hasher.decrypt(
            appointment.patient.contragent.patronymic
        )

    patient_info = PatientFlatForAppointmentList(
        name=appointment.patient.contragent.name,
        last_name=appointment.patient.contragent.last_name,
        patronymic=appointment.patient.contragent.patronymic,
    )
    return patient_info


@SessionContext()
async def hsn_appointment_by_id(doctor_id: int, appointment_id: int):

    query: Select = (
        select(AppointmentDBModel)
        .where(
            AppointmentDBModel.is_deleted.is_(False),
            AppointmentDBModel.id == appointment_id,
        )
        .options(
            selectinload(AppointmentDBModel.patient).selectinload(
                PatientDBModel.contragent
            )
        )
        .options(
            selectinload(AppointmentDBModel.block_complaint),
            selectinload(AppointmentDBModel.block_ekg),
            selectinload(AppointmentDBModel.block_diagnose),
            selectinload(AppointmentDBModel.block_laboratory_test),
            selectinload(AppointmentDBModel.block_complaint),
            selectinload(AppointmentDBModel.block_clinical_condition),
        )
        .options(
            selectinload(AppointmentDBModel.purposes)
            .selectinload(AppointmentPurposeDBModel.medicine_prescriptions)
            .selectinload(MedicinesPrescriptionDBModel.drug)
            .selectinload(DrugDBModel.drug_group)
        )
    )

    cursor: Result = await db_session.execute(query)
    appointment: AppointmentDBModel = cursor.scalars().first()

    if not appointment:
        raise NotFoundException(
            message="Прием c id:{} не найден".format(appointment_id)
        )

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException(
            message="У вас нет прав для доступа к приему с id:{}".format(appointment_id)
        )

    patient_info = await build_patient_info(appointment)

    appointment_model = PatientAppointmentByIdDto(
        id=appointment.id,
        doctor_id=appointment.doctor_id,
        patient=PatientInfoDto(
            id=appointment.patient.id,
            name=patient_info.name,
            last_name=patient_info.last_name,
            patronymic=patient_info.patronymic or "",
            birth_date=contragent_hasher.decrypt(
                appointment.patient.contragent.birth_date
            ),
            gender=appointment.patient.gender,
            location=appointment.patient.location,
            district=appointment.patient.district,
            address=appointment.patient.address,
            phone=appointment.patient.phone,
            clinic=appointment.patient.clinic,
            referring_doctor=appointment.patient.referring_doctor,
            referring_clinic_organization=appointment.patient.referring_clinic_organization,
            disability=appointment.patient.disability,
            lgota_drugs=appointment.patient.lgota_drugs,
            has_hospitalization=appointment.patient.has_hospitalization,
            count_hospitalization=appointment.patient.count_hospitalization,
            last_hospitalization_date=appointment.patient.last_hospitalization_date,
        ),
        date=appointment.date,
        date_next=str(appointment.date_next) if appointment.date_next else None,
        block_clinic_doctor=appointment.block_clinic_doctor,
        block_diagnose=appointment.block_diagnose,
        block_laboratory_test=appointment.block_laboratory_test,
        block_ekg=appointment.block_ekg,
        block_complaint=appointment.block_complaint,
        block_clinical_condition=appointment.block_clinical_condition,
        purposes=[
            AppointmentPurposeFlat(
                id=model.id,
                medicine_prescriptions=[
                    MedicinePrescriptionFlat(
                        id=mp.id,
                        drug=MedicineGroupFlat(
                            id=mp.drug.id,
                            name=mp.drug.name,
                            drug_group_name=mp.drug.drug_group.name,
                        ),
                        dosa=mp.dosa,
                        note=mp.note,
                    )
                    for mp in model.medicine_prescriptions
                ],
            )
            for model in appointment.purposes
        ],
        status=appointment.status,
    )

    return appointment_model
