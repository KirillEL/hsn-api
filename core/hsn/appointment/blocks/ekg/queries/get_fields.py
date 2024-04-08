from sqlalchemy import inspect

from core.hsn.appointment.blocks.complaint.model import AppointmentBlockBooleanFieldsResponse
from shared.db.models.appointment.blocks.block_ekg import AppointmentEkgBlockDBModel
from shared.db.db_session import SessionContext


@SessionContext()
async def hsn_get_block_ekg_fields():
    inspector = inspect(AppointmentEkgBlockDBModel)
    field_responses = []

    display_names = {
        "sinus_ritm": "Синусовый ритм",
        "av_blokada": "AV блокада 2/3 степени",
        "hypertrofia_lg": "Гипертрофия ЛЖ",
        "ritm_eks": "Ритм ЭКС",
        "av_uzlovaya_tahikardia": "AV-узловая тахикардия",
        "superventrikulyrnaya_tahikardia": "Супервентрикулярная тахикардия",
        "zheludochnaya_tahikardia": "Желудочная тахикардия",
        "fabrilycia_predcerdiy": "Фибрилляция предсердий",
        "trepetanie_predcerdiy": "Трепетание предсердий",
        "local_hypokines": "Локальный гипокинез",
        "difusal_hypokines": "Дифунзный гипогинез",
        "distol_disfunction": "Диастолическая дизфункция ",
        "valvular_lesions": "Клапанные поражения",
        "anevrizma": "Аневризма"
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

    for column in inspector.columns.values():
        field_name = column.name
        if field_name not in exclude_fields:
            field_response = AppointmentBlockBooleanFieldsResponse(
                name=field_name,
                displayName=display_names.get(field_name, ""),
                value=None
            )
            field_responses.append(field_response)

    return field_responses