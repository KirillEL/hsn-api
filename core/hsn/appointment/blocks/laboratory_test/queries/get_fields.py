from loguru import logger
from sqlalchemy import inspect

from core.hsn.appointment.blocks.base_model import AppointmentBlockTextDateFieldsResponse, \
    AppointmentBlockTextDateLaboratoryTestFieldsResponse, BaseTextDateField
from shared.db.models.appointment.blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel
from shared.db.db_session import SessionContext


@SessionContext()
async def hsn_get_block_laboratory_test_fields():
    inspector = inspect(AppointmentLaboratoryTestBlockDBModel)
    all_columns = inspector.columns.keys()

    display_names = {
        "nt_pro_bnp": "NT-pro BNP",
        "nt_pro_bnp_date": "NT-pro BNP дата",
        "hbalc": "HbAlC",
        "hbalc_date": "HbAlC дата",
        "eritrocit": "Эритроциты",
        "eritrocit_date": "Эритроциты дата",
        "hemoglobin": "Гемоглобин",
        "hemoglobin_date": "Гемоглобин дата",
        "tg": "ТГ",
        "tg_date": "ТГ дата",
        "lpvp": "ЛПВП",
        "lpvp_date": "ЛПВП дата",
        "lpnp": "ЛПНП",
        "lpnp_date": "ЛПНП дата",
        "general_hc": "Общий ХС",
        "general_hc_date": "Общий ХС дата",
        "natriy": "Натрий",
        "natriy_date": "Натрий дата",
        "kaliy": "Калий",
        "kaliy_date": "Калий дата",
        "glukoza": "Глюкоза",
        "glukoza_date": "Глюкоза дата",
        "mochevaya_kislota": "Мочевая",
        "mochevaya_kislota_date": "Мочевая кислота дата",
        "skf": "СКФ",
        "skf_date": "СКФ дата",
        "kreatinin": "Креатинин",
        "kreatinin_date": "Креатинин дата",
        "protein": "Белок",
        "protein_date": "Белок дата",
        "urine_eritrocit": "Эритроциты",
        "urine_eritrocit_date": "Эритроциты дата",
        "urine_leycocit": "Лейкоциты",
        "urine_leycocit_date": "Лейкоциты дата",
        "microalbumuria": "Микроальбуминурия",
        "microalbumuria_date": "Микроальбуминурия дата"
    }

    categories = {
        "hormonal_blood_analysis": ["nt_pro_bnp", "nt_pro_bnp_date", "hbalc",
                                    "hbalc_date"],
        "general_blood_analysis": ["hemoglobin", "hemoglobin_date", "eritrocit", "eritrocit_date"],
        "blood_chemistry": ["lpnp", "lpnp_date", "general_hc", "general_hc_date", "natriy", "natriy_date", "kaliy",
                            "kaliy_date", "glukoza", "glukoza_date", "mochevaya_kislota", "mochevaya_kislota_date",
                            "skf", "skf_date", "kreatinin", "kreatinin_date", "tg", "tg_date", "lpvp", "lpvp_date"],
        "general_urine_analysis": ["protein", "protein_date", "urine_eritrocit", "urine_eritrocit_date",
                                   "urine_leycocit", "urine_leycocit_date", "microalbumuria", "microalbumuria_date"]
    }

    response = AppointmentBlockTextDateLaboratoryTestFieldsResponse()

    for category_name, fields in categories.items():
        category_list = []
        for field in fields:
            if field in display_names:
                text_name = field
                date_name = field + "_date"
                display_name = display_names[field]
                if text_name in all_columns and date_name in all_columns:
                    field_data = BaseTextDateField(textName=text_name, displayName=display_name, dateName=date_name)
                    category_list.append(field_data)
        setattr(response, category_name, category_list)
    return response.dict()
