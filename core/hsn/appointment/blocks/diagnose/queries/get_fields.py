from core.hsn.appointment.blocks.base_model import AppointmentBlockBooleanTextFieldsResponse
from shared.db.db_session import SessionContext
from shared.db.models.appointment.blocks.block_diagnose import AppointmentDiagnoseBlockDBModel
from sqlalchemy import inspect


@SessionContext()
async def hsn_query_block_diagnose_fields():
    inspector = inspect(AppointmentDiagnoseBlockDBModel)
    field_responses = []

    display_names = {
        "cardiomyopathy": "Кардиомиопатия",
        "cardiomyopathy_note": "Кардиомиопатия примечание",
        "ad": "АД / ГБ",
        "ad_note": "АД примечание",
        "ibc_pikc": "ИБС. ПИКС",
        "ibc_pikc_note": "ИБС. ПИКС примечание",
        "hobl_ba": "ХОБЛ, БА",
        "hobl_ba_note": "ХОБЛ, БА примечание",
        "ibc_stenocardia_napr": "ИБС стенокардия напр.",
        "ibc_stenocardia_napr_note": "ИБС стенокардия напр. примечание",
        "onmk_tia": "ОНМК / ТИА",
        "onmk_tia_note": "ОНМК / ТИА примечание",
        "ibc_another": "ИБС другое",
        "ibc_another_note": "ИБС другое примечание",
        "hbp": "ХБП",
        "hbp_note": "ХБП примечание",
        "fp_tp": "ФП/ТП",
        "fp_tp_note": "ФП/ТП примечание",
        "another": "Другое",
        "another_note": "Другое примечание",
        "dislipidemia": "Дислипидемия",
        "dislipidemia_note": "Дислипидемия примечание",
    }

    exclude_fields = {
        "id",
        "diagnose",
        "classification_func_classes",
        "classification_adjacent_release",
        "classification_nc_stage",
    }

    columns_list = list(inspector.columns.values())

    columns_list_sorted = sorted(
        [column for column in columns_list if column.name in display_names],
        key=lambda col: list(display_names.keys()).index(col.name)
    )

    for column in columns_list_sorted:

        field_name = column.name
        if field_name not in exclude_fields:
            displayName = display_names.get(field_name, "")
            textName = f"{field_name}_note" if field_name + "_note" in display_names else ""

            field_responses.append(AppointmentBlockBooleanTextFieldsResponse(
                booleanName=field_name,
                displayName=displayName,
                textName=textName
            ))

    return field_responses
