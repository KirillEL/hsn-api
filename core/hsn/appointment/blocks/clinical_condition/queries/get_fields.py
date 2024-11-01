from core.hsn.appointment.blocks.complaint.model import AppointmentBlockBooleanFieldsResponse
from shared.db.db_session import SessionContext
from shared.db.models.appointment.blocks.block_clinical_condition import AppointmentClinicalConditionBlockDBModel
from sqlalchemy import inspect


@SessionContext()
async def hsn_query_block_clinical_condition_fields():
    inspector = inspect(AppointmentClinicalConditionBlockDBModel)
    field_responses = []

    display_names = {
        "orthopnea": "Ортопноэ",
        "paroxysmal_nocturnal_dyspnea": "Пароксизмальная ночная одышка",
        "reduced_exercise_tolerance": "Снижение толерантности к нагрузкам",
        "weakness_fatigue": "Слабость",
        "peripheral_edema": "Периферические отеки",
        "ascites": "Асцит",
        "hydrothorax": "Гидроторакс",
        "hydropericardium": "Гидроперикард",
        "night_cough": "Ночной кашель",
        "weight_gain_over_2kg": "Прибавка в весе (более 2кг)",
        "weight_loss": "Потеря веса",
        "depression": "Депрессия",
        "third_heart_sound": "Третий тон (ритм галопа)",
        "apical_impulse_displacement_left": "Смещение верхучечного толчка влево",
        "moist_rales_in_lungs": "Влажные хрипы в легких",
        "heart_murmurs": "Шумы в сердце",
        "tachycardia": "Тахикардия",
        "irregular_pulse": "Нерегулярный пульс",
        "tachypnea": "Тахипное (ЧДД более 16/мин)",
        "hepatomegaly": "Гепатомегалия"
    }

    exclude_fields = {
        "id",
        "other_symptoms",
        "height",
        "weight",
        "bmi",
        "systolic_bp",
        "diastolic_bp",
        "heart_rate",
        "six_min_walk_distance"
    }

    for column in inspector.columns.values():
        field_name = column.name
        if field_name not in exclude_fields:
            field_response = AppointmentBlockBooleanFieldsResponse(
                name=field_name,
                displayName=display_names.get(field_name, ""),
                secondName=""
            )
            field_responses.append(field_response)

    return field_responses
