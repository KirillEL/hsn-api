from io import BytesIO
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse
from openpyxl import Workbook
from api.exceptions import NotFoundException
from core.hsn.appointment import (
    hsn_query_appointment_with_blocks_list,
    HsnAppointmentListContext,
)
from core.hsn.appointment.blocks.clinical_condition import (
    AppointmentClinicalConditionBlock,
)
from core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock

# Заголовки Excel-файла
EXCEL_HEADERS = [
    "ID",
    "ID Врача",
    "ФИО",
    "Дата приема",
    "Дата след приема",
    # patient info
    # "Направивший врач", "Организация", "Кат инвалидности", "Льгота препараты",
    # "Госпитализации", "Кол-во госпитализаций", "Дата последней госпитализации",
    # block_diagnose
    "Диагноз",
    "Класс. по функц классу",
    "Класс. по фракции выброса",
    "Класс. по стадии НК",
    "Кардиомиопатия",
    "Примечание",
    "ИБС ПИКС",
    "Примечание",
    # block_laboratory_test
    "NT-pro BNP",
    "Дата",
    "Гликированный гемоглобин",
    "Дата",
    "Гемоглобин",
    "Эритроциты",
    "ОАК дата",
    "ЛПНП",
    "ЛПВП",
    "Глюкоза",
    "Общий ХС",
    "Калий",
    "Натрий",
    "ТГ",
    "СКФ",
    "Креатинин",
    "Мочевая",
    "Биохимия дата",
    "Белок",
    "Эритроциты",
    "Микроальбуминурия",
    "Лейкоциты",
    "АМ Дата",
    "Примечание",
    # block_ekg
    "Дата экг",
    "Синусовый ритм",
    "AV блокада",
    "Гипертрофия ЛЖ",
    "Ритм ЭКС",
    "AV-узловая тахикардия",
    "Супервентрикулярная тахикардия",
    "Желудочковая тахикардия",
    "Фабрилляция предсердий",
    "Трепетание предсердий",
    "Другие изменения",
    "Дата эхокг",
    "ФВ",
    "СДЛА",
    "ЛП_1",
    "ЛП_2",
    "ПП_1",
    "ПП_2",
    "МЖП",
    "КДР_ЛЖ",
    "КСР_ЛЖ",
    "КДО_ЛЖ",
    "КСО_ЛЖ",
    "ЗСЛЖ",
    "Локальный гипокинез",
    "Дифузный гипокинез",
    "Диастолическая дизфункция",
    "Клапанные поражения",
    "Аневризма",
    "Заключение",
    # block_complaint
    "Утомляемость",
    "Одышка",
    "Повышение АД",
    "Учащенное сердцебиение",
    "Перебои в области сердца",
    "Слабость",
    "Отеки",
    "Примечание",
    # block_clinical_condition
    "Рост",
    "Вес",
    "ИМТ",
    "Сист АД",
    "Диаст АД",
    "ЧСС",
    "Дист 6мин ходьбы",
    "Ортопноэ",
    "Влажные хрипы в легких",
    "Периферические отеки",
    "Гидроторакс",
    "Ночной кашель",
    "Шумы в сердце",
    "Гепатомегалия",
    "Смещение верхучечного толчка влево",
    "Тахикардия",
    "Тахипное",
    "Асцит",
    "Пароксизмальная ночная одышка",
    "Гидроперикард",
    "Третий тон",
    "Нерегулярный пульс",
    "Слабость",
    "Депрессия",
    "Снижение толерантности к нагрузками",
    "Потеря веса",
    "Прибавка в весе (более 2кг в нед)",
    "Примечание",
]


# Функции для извлечения данных по блокам (пример)
def extract_general_info(appointment):
    return [
        appointment.id,
        appointment.doctor_id,
        appointment.full_name,
        appointment.date,
        appointment.date_next or "",
    ]


def extract_clinic_doctor_info(block):
    return [
        block.reffering_doctor or "",
        block.reffering_clinic_organization or "",
        block.disability or "",
        block.lgota_drugs or "",
        block.has_hospitalization or "",
        block.count_hospitalization or "",
        block.last_hospitalization_date or "",
    ]


def extract_diagnose_info(block):
    return [
        block.diagnose or "",
        block.classification_func_classes or "",
        block.classification_adjacent_release or "",
        block.classification_nc_stage or "",
        block.cardiomyopathy or "",
        block.cardiomyopathy_note or "",
        block.ibc_pikc or "",
        block.ibc_pikc_note or "",
    ]


def extract_laboratory_test_info(block: AppointmentLaboratoryTestBlock):
    return [
        block.nt_pro_bnp or "",
        block.nt_pro_bnp_date or "",
        block.hbalc or "",
        block.hbalc_date or "",
        block.eritrocit or "",
        block.hemoglobin or "",
        block.oak_date or "",
        block.tg or "",
        block.lpvp or "",
        block.lpnp or "",
        block.general_hc or "",
        block.natriy or "",
        block.kaliy or "",
        block.glukoza or "",
        block.mochevaya_kislota or "",
        block.skf or "",
        block.kreatinin or "",
        block.bk_dat or "",
        block.protein or "",
        block.urine_eritrocit or "",
        block.urine_leycocit or "",
        block.microalbumuria or "",
        block.am_date or "",
        block.note or "",
    ]


def extract_complaint_info(block: AppointmentComplaintBlock):
    return [
        block.has_fatigue or "",
        block.has_dyspnea or "",
        block.increased_ad or "",
        block.rapid_heartbeat or "",
        block.has_swelling_legs or "",
        block.has_weakness or "",
        block.has_orthopnea or "",
        block.heart_problems or "",
        block.note or "",
    ]


def extract_block_clinical_condition_info(block: AppointmentClinicalConditionBlock):
    return [
        block.orthopnea or "",
        block.paroxysmal_nocturnal_dyspnea or "",
        block.reduced_exercise_tolerance or "",
        block.weakness_fatigue or "",
        block.peripheral_edema or "",
        block.ascites or "",
        block.hydrothorax or "",
        block.hydropericardium or "",
        block.night_cough or "",
        block.weight_gain_over_2kg or "",
        block.weight_loss or "",
        block.depression or "",
        block.third_heart_sound or "",
        block.apical_impulse_displacement_left or "",
        block.moist_rales_in_lungs or "",
        block.heart_murmurs or "",
        block.tachycardia or "",
        block.irregular_pulse or "",
        block.tachypnea or "",
        block.hepatomegaly or "",
        block.other_symptoms or "",
        block.height or "",
        block.weight or "",
        block.bmi or "",
        block.systolic_bp or "",
        block.diastolic_bp or "",
        block.heart_rate or "",
        block.six_min_walk_distance or "",
    ]


def extract_block_ekg_info(block: AppointmentEkgBlock):
    return [
        block.date_ekg or "",
        block.sinus_ritm or "",
        block.av_blokada or "",
        block.hypertrofia_lg or "",
        block.ritm_eks or "",
        block.av_uzlovaya_tahikardia or "",
        block.superventrikulyrnaya_tahikardia or "",
        block.zheludochnaya_tahikardia or "",
        block.fabrilycia_predcerdiy or "",
        block.trepetanie_predcerdiy or "",
        block.another_changes or "",
        block.date_echo_ekg or "",
        block.fv or "",
        block.sdla or "",
        block.lp or "",
        block.lp2 or "",
        block.pp or "",
        block.pp2 or "",
        block.kdr_lg or "",
        block.ksr_lg or "",
        block.kdo_lg or "",
        block.kso_lg or "",
        block.mgp or "",
        block.zslg or "",
        block.local_hypokines or "",
        block.difusal_hypokines or "",
        block.distol_disfunction or "",
        block.valvular_lesions or "",
        block.anevrizma or "",
        block.note or "",
    ]


# Главная функция для экспорта в Excel
async def export_all_appointments(request: Request, doctor_id: int):
    context = HsnAppointmentListContext(doctor_id=doctor_id)
    result = await hsn_query_appointment_with_blocks_list(context)

    if not result:
        raise NotFoundException

    appointments = result

    # Создаем новый Excel-файл
    wb = Workbook()
    ws = wb.active
    ws.title = "Appointments"

    # Записываем заголовки
    ws.append(EXCEL_HEADERS)

    # Записываем данные
    for appointment in appointments:
        row = []
        row.extend(extract_general_info(appointment))
        row.extend(extract_diagnose_info(appointment.block_diagnose))
        row.extend(extract_laboratory_test_info(appointment.block_laboratory_test))
        row.extend(extract_block_ekg_info(appointment.block_ekg))
        row.extend(extract_complaint_info(appointment.block_complaint))
        row.extend(
            extract_block_clinical_condition_info(
                appointment.block_clinical_condition
            )
        )
        ws.append(row)

    # Сохраняем Excel-файл в буфер
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    # Отправляем файл как ответ
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=appointments.xlsx"},
    )
