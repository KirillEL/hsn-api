from loguru import logger
from sqlalchemy import select

from api.exceptions import NotFoundException
from core.hsn.patient.model import PatientTableColumns, PatientTableResponse
from shared.db.models.patient_columns import PatientTableColumnsDBModel
from shared.db.db_session import db_session, SessionContext

default_payload = [
    {
        "title": 'ID',
        "dataIndex": 'id',
        "key": '1',
        "dataType": "string",
        "canBeNull": False,
        "sorter": True,
        "width": 200,
    },
    {
        "title": 'ФИО',
        "dataIndex": 'full_name',
        "key": '2',
        "dataType": "string",
        "canBeNull": False,
        "filter": "searchTableFilter",
        "sorter": True,
        "width": 200,
    },
    {
        "title": 'Пол',
        "dataIndex": 'gender',
        "key": '3',
        "dataType": "string",
        "canBeNull": False,
        "sorter": False,
        "filter": [
            {"text": 'М', "value": 'М'},
            {"text": 'Ж', "value": 'Ж'}
        ],
        "width": 70,
    },
    {
        "title": 'Возраст',
        "dataIndex": 'age',
        "key": '4',
        "dataType": "string",
        "canBeNull": False,
        "filter": "intervalTableFilter",
        "sorter": True,
        "width": 110,
    },
    {
        "title": 'Дата рождения',
        "dataIndex": 'birth_date',
        "key": '5',
        "dataType": "date",
        "canBeNull": False,
        "filter": "dateTableFilter",
        "sorter": True,
        "width": 130,
    },
    {
        "title": 'Дата смерти',
        "dataIndex": 'dod',
        "key": '6',
        "dataType": "date",
        "canBeNull": True,
        "filter": "dateTableFilter",
        "sorter": False,
        "width": 150,
    },
    {
        "title": 'Место жительства',
        "dataIndex": 'location',
        "key": '7',
        "dataType": "string",
        "canBeNull": False,
        "filter": [
            {"text": 'НСО', "value": 'НСО'},
            {"text": 'Новосиюирск', "value": 'Новосибирск'},
            {"text": 'другое', "value": 'другое'}
        ],
        "sorter": False,
        "width": 130,
    },
    {
        "title": 'Район',
        "dataIndex": 'district',
        "key": '8',
        "dataType": "string",
        "canBeNull": False,
        "sorter": False,
        "width": 130,
    },
    {
        "title": 'Адрес',
        "dataIndex": 'address',
        "key": '9',
        "dataType": "address",
        "canBeNull": False,
        "sorter": False,
        "width": 300,
    },
    {
        "title": 'Телефон',
        "dataIndex": 'phone',
        "key": '10',
        "dataType": "phone",
        "canBeNull": False,
        "sorter": False,
        "width": 120,
    },
    {
        "title": 'Поликлиника',
        "dataIndex": 'clinic',
        "key": '11',
        "dataType": "string",
        "canBeNull": False,
        "sorter": False,
        "width": 150,
    },
    {
        "title": 'Примечание',
        "dataIndex": 'patient_note',
        "key": '12',
        "dataType": "string",
        "canBeNull": True,
        "sorter": False,
        "width": 150,
    },
    {
        "title": 'Направивший врач',
        "dataIndex": 'referring_doctor',
        "key": '13',
        "dataType": "string",
        "canBeNull": True,
        "filter": "searchTableFilter",
        "sorter": False,
        "width": 200,
    },
    {
        "title": 'Направившая мед. организация',
        "dataIndex": 'referring_clinic_organization',
        "key": '14',
        "dataType": "string",
        "canBeNull": True,
        "filter": "searchTableFilter",
        "sorter": False,
        "width": 160,
    },
    {
        "title": 'Категория инвалидности',
        "dataIndex": 'disability',
        "key": '15',
        "dataType": "string",
        "canBeNull": False,
        "filter": [
            {"text": 'нет', "value": 'нет'},
            {"text": 'I', "value": 'I'},
            {"text": 'II', "value": 'II'},
            {"text": 'III', "value": 'III'},
            {"text": 'отказ', "value": 'отказ'}
        ],
        "sorter": False,
        "width": 160,
    },
    {
        "title": 'Льготное обеспечение препаратами',
        "dataIndex": 'lgota_drugs',
        "key": '16',
        "dataType": "string",
        "canBeNull": False,
        "filter": [
            {"text": 'нет', "value": 'нет'},
            {"text": 'да', "value": 'да'},
            {"text": 'ССЗ', "value": 'ССЗ'}
        ],
        "sorter": False,
        "width": 130,
    },
    {
        "title": 'Госпитализации',
        "dataIndex": 'has_hospitalization',
        "key": '17',
        "dataType": "boolean",
        "canBeNull": False,
        "filter": [
            {"text": 'Да', "value": 'true'},
            {"text": 'Нет', "value": 'false'}
        ],
        "sorter": False,
        "width": 140,
    },
    {
        "title": 'Количество госпитализаций',
        "dataIndex": 'count_hospitalization',
        "key": '18',
        "dataType": "string",
        "canBeNull": True,
        "filter": "searchTableFilter",
        "sorter": False,
        "width": 150,
    },
    {
        "title": 'Дата последней госпитализации',
        "dataIndex": 'last_hospitalization_date',
        "key": '19',
        "dataType": "date",
        "canBeNull": True,
        "filter": "dateTableFilter",
        "sorter": True,
        "width": 180,
    }
]


@SessionContext()
async def hsn_query_patient_columns(user_id: int):
    query = (
        select(PatientTableColumnsDBModel.table_columns)
        .where(PatientTableColumnsDBModel.user_id == user_id)
    )
    cursor = await db_session.execute(query)
    patient_table_columns = cursor.scalars().first()
    if not patient_table_columns:
        return default_payload
    logger.debug(f'settings: {patient_table_columns}')

    patient_data_indices = {col["dataIndex"] for col in patient_table_columns}

    for column in default_payload:
        data_index = column["dataIndex"]
        for patient_col in patient_table_columns:
            if data_index == patient_col["dataIndex"]:
                if patient_col.get("hidden", False):
                    column["hidden"] = True
                elif "hidden" in column:
                    del column["hidden"]

    filtered_payload = [
        column for column in default_payload if column["dataIndex"] in patient_data_indices
    ]

    title_to_key_map = {col["dataIndex"]: i + 1 for i, col in enumerate(patient_table_columns)}

    for column in filtered_payload:
        title = column["dataIndex"]
        if title in title_to_key_map:
            column["key"] = str(title_to_key_map[title])

    sorted_payload = sorted(filtered_payload, key=lambda x: int(x["key"]))
    logger.debug(f'sorted_payload: {sorted_payload}')
    return sorted_payload

    # patient_data_indices = {col["dataIndex"] for col in patient_table_columns}
    #
    # filtered_payload = [
    #     column for column in default_payload if column["dataIndex"] in patient_data_indices
    # ]
    #
    # title_to_key_map = {col["dataIndex"]: i + 1 for i, col in enumerate(patient_table_columns)}
    #
    # for column in filtered_payload:
    #     title = column["dataIndex"]
    #     if title in title_to_key_map:
    #         column["key"] = str(title_to_key_map[title])
    #
    # sorted_payload = sorted(filtered_payload, key=lambda x: int(x["key"]))
    # logger.debug(f'sorted_payload: {sorted_payload}')
    # return sorted_payload
