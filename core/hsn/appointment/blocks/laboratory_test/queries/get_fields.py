from sqlalchemy import inspect

from core.hsn.appointment.blocks.base_model import AppointmentBlockTextDateFieldsResponse
from shared.db.models.appointment.blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel
from shared.db.db_session import SessionContext


@SessionContext()
async def hsn_get_block_laboratory_test_fields():
    inspector = inspect(AppointmentLaboratoryTestBlockDBModel)
    field_responses = []

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


    exclude_fields = {
        "id",
        "date_ekg",
        "another_changes",
        "date_echo_ekg",
        "fv",
        "sdla",
        "lp",
        "pp",
        "kdr_lg",
        "ksr_lg",
        "kdo_lg",
        "mgp",
        "zslg",
        "note"
    }

    columns_list = list(inspector.columns.values())
    for index, column in enumerate(columns_list):
        if index % 2 == 1:
            field_name = column.name
            if field_name not in exclude_fields:
                textName = display_names.get(field_name, "")
                dateName = f"{field_name}_date" if field_name + "_date" in display_names else ""

                field_responses.append(AppointmentBlockTextDateFieldsResponse(
                    textName=textName,
                    displayName=display_names.get(field_name, ""),
                    dateName=dateName,
                    textValue=None,
                    dateValue=None
                ))

    return field_responses
