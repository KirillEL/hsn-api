from domains.core.hsn.patient.model import PatientAvailableColumnsResponse
from domains.shared.db.db_session import SessionContext


@SessionContext()
async def hsn_query_patient_available_columns():
    available_patient_columns = [
        {"title": "ID", "value": "id", "disabled": True},
        {"title": "ФИО", "value": "full_name", "disabled": True},
        {"title": "Пол", "value": "gender"},
        {"title": "Возраст", "value": "age"},
        {"title": "Дата рождения", "value": "birth_date"},
        {"title": "Дата смерти", "value": "dod"},
        {"title": "Место жительства", "value": "location"},
        {"title": "Район", "value": "district"},
        {"title": "Адрес", "value": "address"},
        {"title": "Телефон", "value": "phone"},
        {"title": "Поликлиника", "value": "clinic"},
        {"title": "Примечание", "value": "patient_note"},
        {"title": "Направивший врач", "value": "referring_doctor"},
        {
            "title": "Направившая мед. организация",
            "value": "referring_clinic_organization",
        },
        {"title": "Категория инвалидности", "value": "disability"},
        {"title": "Льготное обеспечение препаратами", "value": "lgota_drugs"},
        {"title": "Госпитализации", "value": "has_hospitalization"},
        {"title": "Количество госпитализаций", "value": "count_hospitalization"},
        {
            "title": "Дата последней госпитализации",
            "value": "last_hospitalization_date",
        },
    ]
    response = [
        PatientAvailableColumnsResponse(**col) for col in available_patient_columns
    ]
    return response
