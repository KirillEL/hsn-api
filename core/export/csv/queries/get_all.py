from io import BytesIO
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse
from openpyxl import Workbook
from api.exceptions import NotFoundException
from core.hsn.appointment import hsn_appointment_list, HsnAppointmentListContext

app = FastAPI()

# Заголовки Excel-файла
EXCEL_HEADERS = [
    "ID", "ID Врача", "ФИО", "Дата приема", "Дата след приема",
    # block_clinic_doctor
    "Направивший врач", "Организация", "Кат инвалидности", "Льгота препараты",
    "Госпитализации", "Кол-во госпитализаций", "Дата последней госпитализации",
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


# Главная функция для экспорта в Excel
@app.get("/export-appointments")
async def export_all_appointments(request: Request, doctor_id: int):
    context = HsnAppointmentListContext(doctor_id=doctor_id)
    result = await hsn_appointment_list(request, context)
    if not result["data"]:
        raise NotFoundException

    appointments = result["data"]

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
            row.extend(extract_clinic_doctor_info(appointment.block_clinic_doctor))
            row.extend(extract_diagnose_info(appointment.block_diagnose))
            # Добавьте остальные блоки данных
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
