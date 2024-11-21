from loguru import logger
from sqlalchemy import inspect
from core.hsn.appointment.blocks.base_model import (
    AppointmentBlockTextDateFieldsResponse,
    AppointmentBlockTextDateLaboratoryTestFieldsResponse,
    BaseTextDateField,
    GeneralBloodAnalysisTextDateField,
    BloodChemistryTextDateField,
    GeneralUrineAnalysisTextDateField,
    BaseTextField,
    HormonalBloodAnalysisTextDateField,
)
from shared.db.models.appointment.blocks.block_laboratory_test import (
    AppointmentLaboratoryTestBlockDBModel,
)
from shared.db.db_session import SessionContext


@SessionContext()
async def hsn_query_block_laboratory_test_fields():
    inspector = inspect(AppointmentLaboratoryTestBlockDBModel)
    all_columns = inspector.columns.keys()

    display_names = {
        "nt_pro_bnp": "NT-pro BNP",
        "hbalc": "Гликированный гемоглобин",
        "eritrocit": "Эритроциты",
        "hemoglobin": "Гемоглобин",
        "tg": "ТГ",
        "lpvp": "ЛПВП",
        "lpnp": "ЛПНП",
        "general_hc": "Общий ХС",
        "natriy": "Натрий",
        "kaliy": "Калий",
        "glukoza": "Глюкоза",
        "mochevaya_kislota": "Мочевая",
        "skf": "СКФ",
        "kreatinin": "Креатинин",
        "protein": "Белок",
        "urine_eritrocit": "Эритроциты",
        "urine_leycocit": "Лейкоциты",
        "microalbumuria": "Микроальбуминурия",
    }

    categories = {
        "hormonal_blood_analysis": ["nt_pro_bnp", "hbalc"],
        "general_blood_analysis": ["hemoglobin", "eritrocit"],
        "blood_chemistry": [
            "lpnp",
            "general_hc",
            "natriy",
            "kaliy",
            "glukoza",
            "mochevaya_kislota",
            "skf",
            "kreatinin",
            "tg",
            "lpvp",
        ],
        "general_urine_analysis": [
            "protein",
            "urine_eritrocit",
            "urine_leycocit",
            "microalbumuria",
        ],
    }

    date_fields = {
        "hormonal_blood_analysis": ["nt_pro_bnp_date", "hbalc_date"],
        "general_blood_analysis": "oak_date",
        "blood_chemistry": "bk_date",
        "general_urine_analysis": "am_date",
    }

    response = AppointmentBlockTextDateLaboratoryTestFieldsResponse()

    for category_name, fields in categories.items():
        category_list = []
        date_name = date_fields[category_name]

        if category_name == "hormonal_blood_analysis":
            # For fields with individual dates
            for field, individual_date in zip(fields, date_name):
                if (
                    field in display_names
                    and field in all_columns
                    and individual_date in all_columns
                ):
                    field_data = HormonalBloodAnalysisTextDateField(
                        textName=field,
                        displayName=display_names[field],
                        dateName=individual_date,
                    )
                    category_list.append(field_data)
            setattr(response, category_name, category_list)

        else:
            # For fields with a shared date
            shared_date = (
                date_name
                if isinstance(date_name, str) and date_name in all_columns
                else None
            )

            # Only proceed if shared_date is not None
            if shared_date:
                field_objects = [
                    BaseTextField(textName=field, displayName=display_names[field])
                    for field in fields
                    if field in display_names and field in all_columns
                ]

                category_data = None
                if category_name == "general_blood_analysis":
                    category_data = GeneralBloodAnalysisTextDateField(
                        fields=field_objects, dateName=shared_date
                    )
                elif category_name == "blood_chemistry":
                    category_data = BloodChemistryTextDateField(
                        fields=field_objects, dateName=shared_date
                    )
                elif category_name == "general_urine_analysis":
                    category_data = GeneralUrineAnalysisTextDateField(
                        fields=field_objects, dateName=shared_date
                    )

                setattr(response, category_name, category_data)

    return response.dict()
