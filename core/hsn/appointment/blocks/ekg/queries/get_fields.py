from sqlalchemy import inspect

from core.hsn.appointment.blocks.complaint.model import AppointmentBlockBooleanFieldsResponse, \
    AppointmentBlockEkgBooleanFieldsResponse
from shared.db.models.appointment.blocks.block_ekg import AppointmentEkgBlockDBModel
from shared.db.db_session import SessionContext


@SessionContext()
async def hsn_query_block_ekg_fields():
    inspector = inspect(AppointmentEkgBlockDBModel)
    response = AppointmentBlockEkgBooleanFieldsResponse()

    ekg_fields = {
        "sinus_ritm", "av_blokada", "hypertrofia_lg", "ritm_eks",
        "av_uzlovaya_tahikardia", "superventrikulyrnaya_tahikardia",
        "zheludochnaya_tahikardia", "fabrilycia_predcerdiy", "trepetanie_predcerdiy"
    }
    echo_ekg_fields = {
        "local_hypokines", "difusal_hypokines", "distol_disfunction",
        "valvular_lesions", "anevrizma"
    }

    echo_ekg_float_fields = {
        "fv", "sdla", "lp", "pp", "kdr_lg", "ksr_lg", "kdo_lg", "kso_lg", "mgp", "zslg"
    }

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
        "distol_disfunction": "Диастолическая дизфункция",
        "valvular_lesions": "Клапанные поражения",
        "anevrizma": "Аневризма",
        "fv": "ФВ",
        "sdla": "СДЛА",
        "lp": "ЛП",
        "pp": "ПП",
        "kdr_lg": "КДР ЛЖ",
        "ksr_lg": "КСР ЛЖ",
        "kdo_lg": "КДО ЛЖ",
        "kso_lg": "КСО ЛЖ",
        "mgp": "МЖП",
        "zslg": "ЗСЛЖ"
    }

    exclude_fields = {"id", "date_ekg", "another_changes", "date_echo_ekg", "note"}

    for column in inspector.columns.values():
        field_name = column.name
        if field_name not in exclude_fields:
            field_response = AppointmentBlockBooleanFieldsResponse(
                name=field_name,
                displayName=display_names.get(field_name, ""),
                secondName=display_names.get(field_name, "") if field_name == "lp" or field_name == "pp" else ""
            )
            if field_name in ekg_fields:
                response.ekg.append(field_response)
            elif field_name in echo_ekg_fields:
                response.echo_ekg.boolean_fields.append(field_response)
            elif field_name in echo_ekg_float_fields:
                response.echo_ekg.float_fields.append(field_response)

    return response
