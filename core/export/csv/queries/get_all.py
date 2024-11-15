from io import BytesIO
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse
from openpyxl import Workbook
from api.exceptions import NotFoundException
from core.hsn.appointment import hsn_query_appointment_with_blocks_list, HsnAppointmentListContext
from core.hsn.appointment.blocks.clinical_condition import AppointmentClinicalConditionBlock
from core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock

# Заголовки Excel-файла
EXCEL_HEADERS = [
    "ID", "ID Врача", "ФИО", "Дата приема", "Дата след приема",
    # patient info
    #"Направивший врач", "Организация", "Кат инвалидности", "Льгота препараты",
    #"Госпитализации", "Кол-во госпитализаций", "Дата последней госпитализации",
    # block_diagnose
    "Диагноз", "Класс. по функц классу", "Класс. по фракции выброса",
    "Класс. по стадии НК", "Кардиомиопатия", "Примечание", "ИБС ПИКС", "Примечание",
    # block_laboratory_test
    "NT-pro BNP", "Дата", "Гликированный гемоглобин", "Дата",
    "Гемоглобин", "Эритроциты", "ОАК дата",
    "ЛПНП", "ЛПВП", "Глюкоза", "Общий ХС",
    "Калий", "Натрий", "ТГ", "СКФ", "Креатинин", "Мочевая",
    "Биохимия дата", "Белок", "Эритроциты", "Микроальбуминурия", "Лейкоциты", "АМ Дата", "Примечание",
    # block_ekg
    "Дата экг", "Синусовый ритм", "AV блокада", "Гипертрофия ЛЖ", "Ритм ЭКС",
    "AV-узловая тахикардия", "Супервентрикулярная тахикардия", "Желудочковая тахикардия",
    "Фабрилляция предсердий", "Трепетание предсердий", "Другие изменения",
    "Дата эхокг", "ФВ", "СДЛА", "ЛП_1", "ЛП_2", "ПП_1", "ПП_2",
    "МЖП", "КДР_ЛЖ", "КСР_ЛЖ", "КДО_ЛЖ", "КСО_ЛЖ", "ЗСЛЖ",
    "Локальный гипокинез", "Дифузный гипокинез", "Диастолическая дизфункция",
    "Клапанные поражения", "Аневризма", "Заключение",
    # block_complaint
    "Утомляемость", "Одышка", "Повышение АД", "Учащенное сердцебиение",
    "Перебои в области сердца", "Слабость", "Отеки", "Примечание",
    # block_clinical_condition
    "Рост", "Вес", "ИМТ", "Сист АД", "Диаст АД", "ЧСС",
    "Дист 6мин ходьбы", "Ортопноэ", "Влажные хрипы в легких", "Периферические отеки",
    "Гидроторакс", "Ночной кашель", "Шумы в сердце", "Гепатомегалия",
    "Смещение верхучечного толчка влево", "Тахикардия", "Тахипное", "Асцит",
    "Пароксизмальная ночная одышка", "Гидроперикард", "Третий тон",
    "Нерегулярный пульс", "Слабость", "Депрессия", "Снижение толерантности к нагрузками",
    "Потеря веса", "Прибавка в весе (более 2кг в нед)", "Примечание"
]


# Функции для извлечения данных по блокам (пример)
def extract_general_info(appointment):
    return [
        appointment.id, appointment.doctor_id, appointment.full_name,
        appointment.date, appointment.date_next
    ]


def extract_clinic_doctor_info(block):
    return [
        block.reffering_doctor, block.reffering_clinic_organization,
        block.disability, block.lgota_drugs,
        block.has_hospitalization, block.count_hospitalization,
        block.last_hospitalization_date
    ]


def extract_diagnose_info(block):
    return [
        block.diagnose, block.classification_func_classes,
        block.classification_adjacent_release, block.classification_nc_stage,
        block.cardiomyopathy, block.cardiomyopathy_note,
        block.ibc_pikc, block.ibc_pikc_note
    ]


def extract_laboratory_test_info(block: AppointmentLaboratoryTestBlock):
    return [
        block.nt_pro_bnp, block.nt_pro_bnp_date,
        block.hbalc, block.hbalc_date,
        block.eritrocit, block.hemoglobin,
        block.oak_date, block.tg,
        block.lpvp, block.lpnp,
        block.general_hc, block.natriy,
        block.kaliy, block.glukoza,
        block.mochevaya_kislota, block.skf,
        block.kreatinin, block.bk_date,
        block.protein, block.urine_eritrocit,
        block.urine_leycocit, block.microalbumuria,
        block.am_date, block.note
    ]

def extract_complaint_info(block: AppointmentComplaintBlock):
    return [
        block.has_fatigue, block.has_dyspnea,
        block.increased_ad, block.rapid_heartbeat,
        block.has_swelling_legs, block.has_weakness,
        block.has_orthopnea, block.heart_problems,
        block.note
    ]

def extract_block_clinical_condition_info(block: AppointmentClinicalConditionBlock):
    return [
        block.orthopnea, block.paroxysmal_nocturnal_dyspnea,
        block.reduced_exercise_tolerance, block.weakness_fatigue,
        block.peripheral_edema, block.ascites,
        block.hydrothorax, block.hydropericardium,
        block.night_cough, block.weight_gain_over_2kg,
        block.weight_loss, block.depression,
        block.third_heart_sound, block.apical_impulse_displacement_left,
        block.moist_rales_in_lungs, block.heart_murmurs,
        block.tachycardia, block.irregular_pulse,
        block.tachypnea, block.hepatomegaly,
        block.other_symptoms, block.height,
        block.weight, block.bmi, block.systolic_bp,
        block.diastolic_bp, block.heart_rate,
        block.six_min_walk_distance
    ]

def extract_block_ekg_info(block: AppointmentEkgBlock):
    return [
        block.date_ekg, block.sinus_ritm,
        block.av_blokada, block.hypertrofia_lg,
        block.ritm_eks, block.av_uzlovaya_tahikardia,
        block.superventrikulyrnaya_tahikardia,
        block.zheludochnaya_tahikardia,
        block.fabrilycia_predcerdiy,
        block.trepetanie_predcerdiy,
        block.another_changes,
        block.date_echo_ekg,
        block.fv, block.sdla, block.lp,
        block.lp2, block.pp, block.pp2,
        block.kdr_lg, block.ksr_lg,
        block.kdo_lg, block.kso_lg,
        block.mgp, block.zslg,
        block.local_hypokines, block.difusal_hypokines,
        block.distol_disfunction, block.valvular_lesions,
        block.anevrizma, block.note
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
        if appointment.status == "completed":
            row = []
            row.extend(extract_general_info(appointment))
            row.extend(extract_diagnose_info(appointment.block_diagnose))
            row.extend(extract_laboratory_test_info(appointment.block_laboratory_test))
            row.extend(extract_block_ekg_info(appointment.block_ekg))
            row.extend(extract_complaint_info(appointment.block_complaint))
            row.extend(extract_block_clinical_condition_info(appointment.block_clinical_condition))
            ws.append(row)

    # Сохраняем Excel-файл в буфер
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    # Отправляем файл как ответ
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=appointments.xlsx"
        }
    )
