from io import BytesIO
from fastapi import Request
from starlette.responses import StreamingResponse
from openpyxl import Workbook
from api.exceptions import NotFoundException
from domains.core.hsn.appointment import (
    hsn_query_appointment_with_blocks_list,
    HsnAppointmentListContext,
)
from domains.core.hsn.appointment.blocks.clinical_condition import (
    AppointmentClinicalConditionBlock,
)
from domains.core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock
from domains.core.hsn.appointment.blocks.diagnose import AppointmentDiagnoseBlock
from domains.core.hsn.appointment.blocks.ekg import AppointmentEkgBlock
from domains.core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock

# Заголовки Excel-файла
EXCEL_HEADERS = [
    "ID",
    "Имя врача",
    "Фамилия врача",
    "ФИО пациента",
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
        appointment.doctor.name,
        appointment.doctor.last_name,
        appointment.full_name,
        appointment.date,
        appointment.date_next if appointment.date_next else "",
    ]


def extract_clinic_doctor_info(block):
    if not block:
        return [""]*7
    return [
        block.reffering_doctor if block.reffering_doctor else "",
        block.reffering_clinic_organization if block.reffering_clinic_organization else "",
        block.disability if block.disability else "",
        block.lgota_drugs if block.lgota_drugs else "",
        block.has_hospitalization if block.has_hospitalization else "",
        block.count_hospitalization if block.count_hospitalization else "",
        block.last_hospitalization_date if block.last_hospitalization_date else "",
    ]


def extract_diagnose_info(block: AppointmentDiagnoseBlock):
    if not block:
        return [""] * 8
    return [
        block.diagnose if block.diagnose else "",
        block.classification_func_classes if block.classification_func_classes else "",
        block.classification_adjacent_release if block.classification_adjacent_release else "",
        block.classification_nc_stage if block.classification_nc_stage else "",
        block.cardiomyopathy if block.cardiomyopathy else "",
        block.cardiomyopathy_note if block.cardiomyopathy_note else "",
        block.ibc_pikc if block.ibc_pikc else "",
        block.ibc_pikc_note if block.ibc_pikc_note else "",
    ]


def extract_laboratory_test_info(block: AppointmentLaboratoryTestBlock):
    if not block:
        return [""]*23
    return [
        block.nt_pro_bnp if block.nt_pro_bnp else "",
        block.nt_pro_bnp_date if block.nt_pro_bnp_date else "",
        block.hbalc if block.hbalc else "",
        block.hbalc_date if block.hbalc_date else "",
        block.eritrocit if block.eritrocit else "",
        block.hemoglobin if block.hemoglobin else "",
        block.oak_date if block.oak_date else "",
        block.tg if block.tg else "",
        block.lpvp if block.lpvp else "",
        block.lpnp if block.lpnp else "",
        block.general_hc if block.general_hc else "",
        block.natriy if block.natriy else "",
        block.kaliy if block.kaliy else "",
        block.glukoza if block.glukoza else "",
        block.mochevaya_kislota if block.mochevaya_kislota else "",
        block.skf if block.skf else "",
        block.kreatinin if block.kreatinin else "",
        block.bk_date if block.bk_date else "",
        block.protein if block.protein else "",
        block.urine_eritrocit if block.urine_eritrocit else "",
        block.urine_leycocit if block.urine_leycocit else "",
        block.microalbumuria if block.microalbumuria else "",
        block.am_date if block.am_date else "",
        block.note if block.note else "",
    ]


def extract_complaint_info(block: AppointmentComplaintBlock):
    if not block:
        return [""]*8
    return [
        block.has_fatigue if block.has_fatigue else "",
        block.has_dyspnea if block.has_dyspnea else "",
        block.increased_ad if not block.increased_ad else "",
        block.rapid_heartbeat if block.rapid_heartbeat else "",
        block.has_swelling_legs if block.has_swelling_legs else "",
        block.has_weakness if block.has_weakness else "",
        block.has_orthopnea if block.has_orthopnea else "",
        block.heart_problems if block.heart_problems else "",
        block.note if block.note else "",
    ]


def extract_block_clinical_condition_info(block: AppointmentClinicalConditionBlock):
    if not block:
        return [""] * 27
    return [
        block.orthopnea if block.orthopnea else "",
        block.paroxysmal_nocturnal_dyspnea if block.paroxysmal_nocturnal_dyspnea else "",
        block.reduced_exercise_tolerance if block.reduced_exercise_tolerance else "",
        block.weakness_fatigue if block.weakness_fatigue else "",
        block.peripheral_edema if block.peripheral_edema else "",
        block.ascites if block.ascites else "",
        block.hydrothorax if block.hydrothorax else "",
        block.hydropericardium if block.hydropericardium else "",
        block.night_cough if block.night_cough else "",
        block.weight_gain_over_2kg if block.weight_gain_over_2kg else "",
        block.weight_loss if block.weight_loss else "",
        block.depression if block.depression else "",
        block.third_heart_sound if block.third_heart_sound else "",
        block.apical_impulse_displacement_left if block.apical_impulse_displacement_left else "",
        block.moist_rales_in_lungs if block.moist_rales_in_lungs else "",
        block.heart_murmurs if block.heart_murmurs else "",
        block.tachycardia if block.tachycardia else "",
        block.irregular_pulse if block.irregular_pulse else "",
        block.tachypnea if block.tachypnea else "",
        block.hepatomegaly if block.hepatomegaly else "",
        block.other_symptoms if block.other_symptoms else "",
        block.height if block.height else "",
        block.weight if block.weight else "",
        block.bmi if block.bmi else "",
        block.systolic_bp if block.systolic_bp else "",
        block.diastolic_bp if block.diastolic_bp else "",
        block.heart_rate if block.heart_rate else "",
        block.six_min_walk_distance if block.six_min_walk_distance else "",
    ]


def extract_block_ekg_info(block: AppointmentEkgBlock):
    if not block:
        return [""]* 29
    return [
        block.date_ekg if block.date_ekg else "",
        block.sinus_ritm if block.sinus_ritm else "",
        block.av_blokada if block.av_blokada else "",
        block.hypertrofia_lg if block.hypertrofia_lg else "",
        block.ritm_eks if block.ritm_eks else "",
        block.av_uzlovaya_tahikardia if block.av_uzlovaya_tahikardia else "",
        block.superventrikulyrnaya_tahikardia if block.superventrikulyrnaya_tahikardia else "",
        block.zheludochnaya_tahikardia if block.zheludochnaya_tahikardia else "",
        block.fabrilycia_predcerdiy if block.fabrilycia_predcerdiy else "",
        block.trepetanie_predcerdiy if block.trepetanie_predcerdiy else "",
        block.another_changes if block.another_changes else "",
        block.date_echo_ekg if block.date_echo_ekg else "",
        block.fv if block.fv else "",
        block.sdla if block.sdla else "",
        block.lp if block.lp else "",
        block.lp2 if block.lp2 else "",
        block.pp if block.pp else "",
        block.pp2 if block.pp2 else "",
        block.kdr_lg if block.kdr_lg else "",
        block.ksr_lg if block.ksr_lg else "",
        block.kdo_lg if block.kdo_lg else "",
        block.kso_lg if block.kso_lg else "",
        block.mgp if block.mgp else "",
        block.zslg if block.zslg else "",
        block.local_hypokines if block.local_hypokines else "",
        block.difusal_hypokines if block.difusal_hypokines else "",
        block.distol_disfunction if block.distol_disfunction else "",
        block.valvular_lesions if block.valvular_lesions else "",
        block.anevrizma if block.anevrizma else "",
        block.note if block.note else "",
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
